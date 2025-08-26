import pytest
import zen
import os
from unittest.mock import patch
from datetime import datetime


class TestWindowRule:
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

    def test_window_evaluation(self):
        input_data = {
            "risk_type": "windows",
            "window_type": "single",
            "vegetation_type": "tree",
            "distance": 80
        }
        
        expected_output = {
            "api_version": "3",
            "performance": "86.5µs",
            "property_id": 1,
            "result": {
                "distance": 80,
                "mitigations": {
                    "bridge": [
                        "Apply a Film to windows which decreases minimum safe distance by 20%",
                        "Apply flame retardants to shrubs that decrease minimum safe distance by 25%",
                        "Prune trees to a safe height decreases safe distance by 50%"
                    ],
                    "full": [
                        "Remove Vegetation",
                        "Replace window with Tempered Glass"
                    ]
                },
                "risk_type": "windows",
                "safe_distance": 30,
                "safe_distance_base": 30,
                "safe_distance_calc": 90,
                "safe_distance_diff": 10,
                "vegetation_type": "tree",
                "window_type": "single"
            },
            "timestamp": "2025-08-26T16:22:53.477796"
        }
        
        # Mock datetime for consistent timestamp
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.fromisoformat("2025-08-26T16:22:53.477796")
            
            # Execute the zen decision
            zen_result = self.decision.evaluate(input_data)
            
            # Mock the performance value to match expected output
            with patch.dict(zen_result, {"performance": "86.5µs"}):
                # Format the result to match expected API response structure
                formatted_result = {
                    "api_version": "3",
                    "performance": zen_result["performance"],
                    "property_id": 1,
                    "result": zen_result["result"],
                    "timestamp": mock_datetime.utcnow().isoformat()
                }
                
                assert formatted_result == expected_output
                assert formatted_result["result"]["distance"] == 80
                assert formatted_result["result"]["risk_type"] == "windows"
                assert formatted_result["result"]["window_type"] == "single"
                assert formatted_result["result"]["vegetation_type"] == "tree"
                assert formatted_result["result"]["safe_distance"] == 30
                assert formatted_result["result"]["safe_distance_base"] == 30
                assert formatted_result["result"]["safe_distance_calc"] == 90
                assert formatted_result["result"]["safe_distance_diff"] == 10
                assert "mitigations" in formatted_result["result"]
                assert "bridge" in formatted_result["result"]["mitigations"]
                assert "full" in formatted_result["result"]["mitigations"]
                assert formatted_result["api_version"] == "3"
                assert formatted_result["property_id"] == 1