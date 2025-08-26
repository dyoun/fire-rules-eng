from flask import Blueprint, request, jsonify
from dependency_injector.wiring import Provide, inject
from ...config.container import Container
from ...domain.interfaces.rules_service import IRulesService
from ...domain.models.rule_evaluation import RuleEvaluationRequest


rules_bp = Blueprint('rules', __name__, url_prefix='/rules')


@rules_bp.route('/versions', methods=['GET'])
@inject
def get_available_versions(
    rules_service: IRulesService = Provide[Container.rules_service]
):
    """Get list of available rule versions."""
    try:
        versions = rules_service.get_available_versions()
        latest = rules_service.get_latest_version()
        
        return jsonify({
            'versions': versions,
            'latest': latest
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get versions: {str(e)}'}), 500


@rules_bp.route('/latest', methods=['POST'])
@inject
def evaluate_rules_latest(
    rules_service: IRulesService = Provide[Container.rules_service]
):
    """Evaluate rules against provided observations using latest version."""
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'observations' not in data:
            return jsonify({'error': 'Missing required field: observations'}), 400
        
        # Validate observations format (must be dict or array of dicts)
        observations = data['observations']
        if not isinstance(observations, (dict, list)):
            return jsonify({'error': 'observations must be an object or array of objects'}), 400
        
        if isinstance(observations, list):
            if not observations:
                return jsonify({'error': 'observations array cannot be empty'}), 400
            for i, obs in enumerate(observations):
                if not isinstance(obs, dict):
                    return jsonify({'error': f'observations[{i}] must be an object'}), 400
        
        # Create domain request object with latest version (None will default to latest)
        rule_request = RuleEvaluationRequest(
            observations=observations,
            version=None,  # This will use latest version
            request_id=data.get('property_id')
        )
        
        # Evaluate rules
        result = rules_service.evaluate_fire_risk(rule_request)
        
        # Return response
        return jsonify({
            'result': result.result,
            'performance': result.performance,
            'timestamp': result.timestamp.isoformat(),
            'api_version': result.api_version,
            'property_id': result.request_id
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid request data: {str(e)}'}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@rules_bp.route('/version/<version>', methods=['POST'])
@inject
def evaluate_rules_versioned(
    version: str,
    rules_service: IRulesService = Provide[Container.rules_service]
):
    """Evaluate rules against provided observations using specified version."""
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'observations' not in data:
            return jsonify({'error': 'Missing required field: observations'}), 400
        
        # Validate observations format (must be dict or array of dicts)
        observations = data['observations']
        if not isinstance(observations, (dict, list)):
            return jsonify({'error': 'observations must be an object or array of objects'}), 400
        
        if isinstance(observations, list):
            if not observations:
                return jsonify({'error': 'observations array cannot be empty'}), 400
            for i, obs in enumerate(observations):
                if not isinstance(obs, dict):
                    return jsonify({'error': f'observations[{i}] must be an object'}), 400
        
        # Create domain request object
        rule_request = RuleEvaluationRequest(
            observations=observations,
            version=version,
            request_id=data.get('property_id')
        )
        
        # Evaluate rules
        result = rules_service.evaluate_fire_risk(rule_request)
        
        # Return response
        return jsonify({
            'result': result.result,
            'performance': result.performance,
            'timestamp': result.timestamp.isoformat(),
            'api_version': result.api_version,
            'property_id': result.request_id
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid request data: {str(e)}'}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500