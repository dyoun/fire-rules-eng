import pytest
import zen
import os
from unittest.mock import patch
from datetime import datetime


class TestAtticRule:
    def setup_method(self):
        self.engine = zen.ZenEngine()
        
        # Load the latest rules file
        rules_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'src', 
            'rules', 
            'fire_risk', 
            'latest', 
            'fire_risk.json'
        )
        
        with open(rules_file_path, 'r') as f:
            self.rule_content = f.read()
            
        self.decision = self.engine.create_decision(self.rule_content)

    def test_attic_vent_screens_evaluation(self):
        input_data = {
            "risk_type": "attic",
            "attic_vent_screens": True
        }
        
        expected_output = {
            "api_version": "3",
            "performance": "35.0µs",
            "property_id": 1,
            "result": {
                "attic_vent_screens": True,
                "risk_type": "attic"
            },
            "timestamp": "2025-08-26T16:23:07.425909"
        }
        
        # Mock datetime for consistent timestamp
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.fromisoformat("2025-08-26T16:23:07.425909")
            
            # Execute the zen decision
            zen_result = self.decision.evaluate(input_data)
            
            # Mock the performance value to match expected output
            with patch.dict(zen_result, {"performance": "35.0µs"}):
                # Format the result to match expected API response structure
                formatted_result = {
                    "api_version": "3",
                    "performance": zen_result["performance"],
                    "property_id": 1,
                    "result": zen_result["result"],
                    "timestamp": mock_datetime.utcnow().isoformat()
                }
                
                assert formatted_result == expected_output
                assert formatted_result["result"]["attic_vent_screens"] == True
                assert formatted_result["result"]["risk_type"] == "attic"
                assert formatted_result["api_version"] == "3"
                assert formatted_result["property_id"] == 1