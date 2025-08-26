#!/usr/bin/env python3
"""
Test script for FireMitigationService
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.application.services.fire_mitigation_service import FireMitigationService


def main():
    # Initialize the service
    mitigation_service = FireMitigationService()
    
    # Test with sample observations
    property_id = "PROP-12345"
    
    # Create observations matching the specified format
    observations = [
        {
            "risk_type": "windows",
            "window_type": "single", 
            "vegetation_type": "tree",
            "distance": 80
        },
        {
            "risk_type": "attic",
            "attic_vent_screens": False
        },
        {
            "risk_type": "roof",
            "roof_type": "c",
            "wild_fire_risk": "a"
        }
    ]
    
    try:
        # Submit to latest version
        print("Submitting observations to latest version...")
        result = mitigation_service.submit_property_observations(
            property_id=property_id,
            observations=observations
        )
        
        print(f"Success! Response:")
        print(f"- API Version: {result.get('api_version')}")
        print(f"- Performance: {result.get('performance')}")
        print(f"- Request ID: {result.get('request_id')}")
        print(f"- Results: {len(result.get('result', []))} evaluations")
        
        # Submit to specific version
        print("\nSubmitting observations to version 3...")
        result_v3 = mitigation_service.submit_property_observations(
            property_id=property_id,
            observations=observations,
            version="3"
        )
        
        print(f"Success! Response:")
        print(f"- API Version: {result_v3.get('api_version')}")
        print(f"- Performance: {result_v3.get('performance')}")
        print(f"- Request ID: {result_v3.get('request_id')}")
        print(f"- Results: {len(result_v3.get('result', []))} evaluations")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()