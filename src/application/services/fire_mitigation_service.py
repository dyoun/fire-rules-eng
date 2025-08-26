import requests
import json
from typing import List, Dict, Any, Optional


class FireMitigationService:
    """Service for submitting fire mitigation observations to the rules engine."""

    def __init__(self, rules_api_base_url: str = "http://localhost:5000"):
        self.rules_api_base_url = rules_api_base_url.rstrip('/')

    def submit_property_observations(
        self,
        property_id: str,
        observations: List[Dict[str, Any]],
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit an array of fire mitigation observations to the rules engine.

        Args:
            property_id: Unique identifier for the property (used as request_id)
            observations: List of observation objects
            version: Optional version to use, defaults to 'latest'

        Returns:
            Dict containing the rules engine response
        """
        if not observations:
            raise ValueError("observations cannot be empty")

        # Prepare the request payload matching the specified format
        payload = {
            'observations': observations,
            'property_id': property_id
        }

        # Determine endpoint URL
        endpoint = f"{self.rules_api_base_url}/rules/latest" if version is None else f"{self.rules_api_base_url}/rules/version/{version}"

        try:
            # Submit to rules engine
            response = requests.post(
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to submit observations to rules engine: {str(e)}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse rules engine response: {str(e)}") from e

    def create_sample_observations(self) -> List[Dict[str, Any]]:
        """
        Create sample fire mitigation observations matching the specified format.

        Returns:
            List of sample observations
        """
        return [
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

    def process_property_risk_assessment(
        self,
        property_id: str,
        window_observations: List[Dict[str, Any]] = None,
        attic_observations: List[Dict[str, Any]] = None,
        roof_observations: List[Dict[str, Any]] = None,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a complete property risk assessment with multiple observation types.

        Args:
            property_id: Unique identifier for the property
            window_observations: List of window-related observations
            attic_observations: List of attic-related observations
            roof_observations: List of roof-related observations
            version: Optional version to use, defaults to 'latest'

        Returns:
            Dict containing the rules engine response
        """
        all_observations = []

        if window_observations:
            all_observations.extend(window_observations)
        if attic_observations:
            all_observations.extend(attic_observations)
        if roof_observations:
            all_observations.extend(roof_observations)

        if not all_observations:
            # Use sample observations if none provided
            all_observations = self.create_sample_observations()

        return self.submit_property_observations(
            property_id=property_id,
            observations=all_observations,
            version=version
        )
