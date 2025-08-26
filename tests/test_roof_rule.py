import pytest
import zen
import os
from unittest.mock import patch
from datetime import datetime


class TestRoofRule:
    def setup_method(self):
        self.engine = zen.ZenEngine()
        
        # Try multiple paths to find the rules file
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'rules', 'fire_risk', 'latest', 'fire_risk.json'),
            os.path.join(os.getcwd(), 'src', 'rules', 'fire_risk', 'latest', 'fire_risk.json'),
            os.path.join(os.getcwd(), 'src', 'rules', 'fire_risk', '3', 'fire_risk.json')
        ]
        
        rules_file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                rules_file_path = path
                break
        
        if rules_file_path is None:
            raise FileNotFoundError("Could not find fire_risk.json in any expected location")
        
        with open(rules_file_path, 'r') as f:
            self.rule_content = f.read()
            
        self.decision = self.engine.create_decision(self.rule_content)

    def test_roof_evaluation(self):
        input_data = {
            "risk_type": "roof",
            "roof_type": "c",
            "wild_fire_risk": "a"
        }
        
        expected_output = {
            "api_version": "3",
            "performance": "48.7µs",
            "property_id": 1,
            "result": {
                "mitigations": "No Mitigation",
                "risk_type": "roof",
                "roof_type": "c",
                "wild_fire_risk": "a"
            },
            "timestamp": "2025-08-26T16:22:38.434683"
        }
        
        # Mock datetime for consistent timestamp
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.fromisoformat("2025-08-26T16:22:38.434683")
            
            # Execute the zen decision
            zen_result = self.decision.evaluate(input_data)
            
            # Mock the performance value to match expected output
            with patch.dict(zen_result, {"performance": "48.7µs"}):
                # Format the result to match expected API response structure
                formatted_result = {
                    "api_version": "3",
                    "performance": zen_result["performance"],
                    "property_id": 1,
                    "result": zen_result["result"],
                    "timestamp": mock_datetime.utcnow().isoformat()
                }
                
                assert formatted_result == expected_output
                assert formatted_result["result"]["mitigations"] == "No Mitigation"
                assert formatted_result["result"]["risk_type"] == "roof"
                assert formatted_result["result"]["roof_type"] == "c"
                assert formatted_result["result"]["wild_fire_risk"] == "a"
                assert formatted_result["api_version"] == "3"
                assert formatted_result["property_id"] == 1