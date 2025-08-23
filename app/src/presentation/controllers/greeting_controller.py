from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from ...domain.interfaces.greeting_service import IGreetingService
from ...config.container import Container


greeting_bp = Blueprint('greeting', __name__, url_prefix='/api/v1')


@greeting_bp.route('/hello', methods=['GET'])
@inject
def get_hello_world(
    greeting_service: IGreetingService = Provide[Container.greeting_service]
):
    """Get a Hello World greeting."""
    try:
        greeting = greeting_service.create_hello_world_greeting()
        return jsonify({
            'id': greeting.id,
            'message': greeting.message,
            'timestamp': greeting.timestamp.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@greeting_bp.route('/greetings', methods=['GET'])
@inject
def get_all_greetings(
    greeting_service: IGreetingService = Provide[Container.greeting_service]
):
    """Get all stored greetings."""
    try:
        greetings = greeting_service.get_all_greetings()
        return jsonify([{
            'id': greeting.id,
            'message': greeting.message,
            'timestamp': greeting.timestamp.isoformat()
        } for greeting in greetings]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@greeting_bp.route('/greetings', methods=['POST'])
@inject
def create_custom_greeting(
    greeting_service: IGreetingService = Provide[Container.greeting_service]
):
    """Create a custom greeting."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        greeting = greeting_service.create_custom_greeting(data['message'])
        return jsonify({
            'id': greeting.id,
            'message': greeting.message,
            'timestamp': greeting.timestamp.isoformat()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500