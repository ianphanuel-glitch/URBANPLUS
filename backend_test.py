import requests
import sys
import json
from datetime import datetime

class UrbanPulseAPITester:
    def __init__(self, base_url="https://metrolytics.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Non-dict response'}")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append({
                    'test': name,
                    'endpoint': endpoint,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:200]
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'test': name,
                'endpoint': endpoint,
                'error': str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_cities_endpoint(self):
        """Test cities list endpoint"""
        success, response = self.run_test("Cities List", "GET", "cities", 200)
        if success and response:
            cities = response.get('cities', [])
            if cities and len(cities) > 0:
                nairobi_found = any(city.get('id') == 'nairobi' for city in cities)
                if nairobi_found:
                    print("   ✅ Nairobi found in cities list")
                else:
                    print("   ⚠️  Nairobi not found in cities list")
            else:
                print("   ⚠️  No cities returned")
        return success

    def test_nairobi_data_endpoint(self):
        """Test Nairobi spatial data endpoint"""
        success, response = self.run_test("Nairobi Spatial Data", "GET", "city/nairobi/data", 200)
        if success and response:
            layers = response.get('layers', {})
            expected_layers = ['residential', 'commercial', 'facilities', 'roads']
            
            for layer in expected_layers:
                if layer in layers:
                    features = layers[layer].get('features', [])
                    print(f"   ✅ {layer.title()} layer: {len(features)} features")
                else:
                    print(f"   ❌ Missing {layer} layer")
        return success

    def test_nairobi_indicators_endpoint(self):
        """Test Nairobi indicators endpoint"""
        success, response = self.run_test("Nairobi Indicators", "GET", "city/nairobi/indicators", 200)
        if success and response:
            indicators = response.get('indicators', {})
            expected_indicators = ['population_density', 'land_use', 'road_network', 'service_accessibility', 'green_space']
            
            for indicator in expected_indicators:
                if indicator in indicators:
                    print(f"   ✅ {indicator.replace('_', ' ').title()} indicator present")
                else:
                    print(f"   ❌ Missing {indicator} indicator")
        return success

    def test_ai_insights_endpoint(self):
        """Test AI insights generation"""
        # First get indicators to use as input
        _, indicators_response = self.run_test("Get Indicators for AI", "GET", "city/nairobi/indicators", 200)
        
        if not indicators_response:
            print("   ❌ Cannot test AI insights without indicators")
            return False
            
        indicators = indicators_response.get('indicators', {})
        
        ai_request = {
            "indicators": indicators,
            "model": "gpt-5.2"
        }
        
        success, response = self.run_test("AI Insights Generation", "POST", "ai/insights", 200, ai_request)
        if success and response:
            if 'error' in response:
                print(f"   ⚠️  AI Error: {response['error']}")
                return False
            else:
                issues = response.get('issues', [])
                recommendations = response.get('recommendations', [])
                print(f"   ✅ Generated {len(issues)} issues and {len(recommendations)} recommendations")
                if response.get('model_used'):
                    print(f"   ✅ Model used: {response['model_used']}")
        return success

def main():
    print("🏙️  UrbanPulse AI Backend API Testing")
    print("=" * 50)
    
    tester = UrbanPulseAPITester()
    
    # Run all tests
    print("\n📡 Testing API Endpoints...")
    
    tester.test_root_endpoint()
    tester.test_cities_endpoint()
    tester.test_nairobi_data_endpoint()
    tester.test_nairobi_indicators_endpoint()
    tester.test_ai_insights_endpoint()
    
    # Print summary
    print(f"\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed / tester.tests_run * 100):.1f}%")
    
    if tester.failed_tests:
        print(f"\n❌ Failed Tests:")
        for failure in tester.failed_tests:
            print(f"   - {failure['test']}: {failure.get('error', f\"Status {failure.get('actual')} (expected {failure.get('expected')})\"}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())