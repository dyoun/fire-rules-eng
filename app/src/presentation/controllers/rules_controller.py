from flask import Blueprint, request, jsonify
from dependency_injector.wiring import Provide, inject
from ...config.container import Container
from ...domain.interfaces.rules_service import IRulesService
from ...domain.models.rule_evaluation import RuleEvaluationRequest


rules_bp = Blueprint('rules', __name__, url_prefix='/rules')


@rules_bp.route('/', methods=['POST'])
@inject
def evaluate_rules(
    rules_service: IRulesService = Provide[Container.rules_service]
):
    """Evaluate rules against provided observations."""
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'observations' not in data:
            return jsonify({'error': 'Missing required field: observations'}), 400
        
        # Create domain request object
        rule_request = RuleEvaluationRequest(
            observations=data['observations'],
            request_id=data.get('request_id')
        )
        
        # Evaluate rules
        result = rules_service.evaluate_fire_risk(rule_request)
        
        # Return response
        return jsonify({
            'result': result.result,
            'performance': result.performance,
            'timestamp': result.timestamp.isoformat(),
            'request_id': result.request_id
        }), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid request data: {str(e)}'}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500