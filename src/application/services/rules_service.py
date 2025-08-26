import json
import os
import zen
from datetime import datetime
from ...domain.interfaces.rules_service import IRulesService
from ...domain.models.rule_evaluation import RuleEvaluationRequest, RuleEvaluationResult


class RulesService(IRulesService):
    """Service implementation for rules engine operations."""

    def __init__(self, rules_base_path: str = None):
        self.engine = zen.ZenEngine()
        # Default to src/rules/fire_risk relative to the service file location
        if rules_base_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.rules_base_path = os.path.join(current_dir, '..', '..', 'rules', 'fire_risk')
        else:
            self.rules_base_path = rules_base_path

    def get_available_versions(self):
        """Get list of available rule versions."""
        try:
            if not os.path.exists(self.rules_base_path):
                return []
            
            versions = []
            for item in os.listdir(self.rules_base_path):
                item_path = os.path.join(self.rules_base_path, item)
                if os.path.isdir(item_path) and item.isdigit():
                    versions.append(item)
            
            return sorted(versions, key=int, reverse=True)  # Latest version first
        except Exception:
            return []

    def get_latest_version(self):
        """Get the latest available version."""
        versions = self.get_available_versions()
        return versions[0] if versions else None

    def load_rules_by_version(self, version: str = None):
        """Load rules JSON content by version."""
        if version is None:
            version = self.get_latest_version()
        
        if version is None:
            raise FileNotFoundError("No rule versions available")
        
        rules_file_path = os.path.join(self.rules_base_path, version, 'fire_risk.json')
        
        if not os.path.exists(rules_file_path):
            raise FileNotFoundError(f"Rules file not found for version {version}: {rules_file_path}")

        with open(rules_file_path, 'r') as f:
            return f.read()

    def evaluate_fire_risk(self, request: RuleEvaluationRequest) -> RuleEvaluationResult:
        """Evaluate fire risk rules against provided observations."""
        try:
            # Determine which version will be used
            version_to_use = request.version
            if version_to_use is None:
                version_to_use = self.get_latest_version()
            
            # Load rule definition by version
            rule_json = self.load_rules_by_version(version_to_use)

            # Create decision from rule definition
            decision = self.engine.create_decision(rule_json)

            # Handle both single observation and array of observations
            if isinstance(request.observations, list):
                # Process array of observations
                results = []
                total_performance_time = 0
                
                for observation in request.observations:
                    result = decision.evaluate(observation)
                    results.append(result.get('result', {}))
                    
                    # Parse performance time for aggregation
                    perf_str = result.get('performance', '0µs')
                    if 'µs' in perf_str:
                        time_val = float(perf_str.replace('µs', ''))
                        total_performance_time += time_val
                
                final_result = results
                performance_str = f"{total_performance_time:.1f}µs"
            else:
                # Process single observation
                result = decision.evaluate(request.observations)
                final_result = result.get('result', {})
                performance_str = result.get('performance', '')

            return RuleEvaluationResult(
                result=final_result,
                performance=performance_str,
                timestamp=datetime.utcnow(),
                api_version=version_to_use,
                request_id=request.request_id
            )
        except Exception as e:
            raise RuntimeError(f"Failed to evaluate rules: {str(e)}") from e
