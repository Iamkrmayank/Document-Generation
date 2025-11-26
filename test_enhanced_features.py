#!/usr/bin/env python3
"""
Test Enhanced Features: Descriptions and Chart/Figure Data
Tests the new description and enhanced chart/figure handling
"""

import json
from template_inference import TemplateInferenceEngine

def test_enhanced_element_analysis():
    """Test enhanced element analysis with descriptions and chart data"""
    print("🧪 Testing Enhanced Element Analysis...")
    
    # Mock bedrock client
    class MockBedrockClient:
        pass
    
    engine = TemplateInferenceEngine(MockBedrockClient())
    
    # Create mock elements with enhanced data
    mock_elements = [
        {
            'element_id': 'e1',
            'type': 'title',
            'text': 'Company Profile 2024',
            'description': 'Main document title that identifies the company profile and establishes brand identity',
            'category': 'document_identity_and_metadata',
            'importance': 'critical',
            'pii_type': 'NONE'
        },
        {
            'element_id': 'e2',
            'type': 'charts_graphs',
            'text': 'Revenue Growth Chart',
            'description': 'Visual representation showing company revenue growth over the past 5 years',
            'chart': {
                'chart_type': 'line',
                'title': 'Revenue Growth 2019-2024',
                'description': 'Shows steady 25% year-over-year revenue growth',
                'data': [
                    {'name': '2019 Revenue', 'value': '10M', 'unit': 'USD'},
                    {'name': '2020 Revenue', 'value': '12.5M', 'unit': 'USD'},
                    {'name': '2021 Revenue', 'value': '15.6M', 'unit': 'USD'},
                    {'name': '2022 Revenue', 'value': '19.5M', 'unit': 'USD'},
                    {'name': '2023 Revenue', 'value': '24.4M', 'unit': 'USD'},
                    {'name': '2024 Revenue', 'value': '30.5M', 'unit': 'USD'}
                ],
                'source': 'Financial Department'
            },
            'category': 'supporting_elements',
            'importance': 'important',
            'pii_type': 'NONE'
        },
        {
            'element_id': 'e3',
            'type': 'figures_images',
            'text': 'Organizational Structure',
            'description': 'Company hierarchy diagram showing leadership structure and reporting lines',
            'figure': {
                'figure_type': 'diagram',
                'title': 'Organizational Chart',
                'description': 'Shows company leadership structure with clear reporting hierarchy',
                'elements': [
                    {'name': 'CEO', 'value': 'Chief Executive Officer - Strategic Leadership'},
                    {'name': 'CTO', 'value': 'Chief Technology Officer - Technical Direction'},
                    {'name': 'CFO', 'value': 'Chief Financial Officer - Financial Management'},
                    {'name': 'VP Sales', 'value': 'Vice President Sales - Revenue Generation'},
                    {'name': 'VP Marketing', 'value': 'Vice President Marketing - Brand Management'}
                ]
            },
            'category': 'supporting_elements',
            'importance': 'important',
            'pii_type': 'PERSON_NAME'
        }
    ]
    
    # Test element pattern analysis
    pattern = engine._analyze_element_pattern(mock_elements)
    
    # Validate enhanced data
    assert 'description' in pattern, "❌ Missing description field"
    assert 'charts' in pattern, "❌ Missing charts field"
    assert 'figures' in pattern, "❌ Missing figures field"
    
    assert len(pattern['charts']) == 1, f"❌ Expected 1 chart, got {len(pattern['charts'])}"
    assert len(pattern['figures']) == 1, f"❌ Expected 1 figure, got {len(pattern['figures'])}"
    
    # Validate chart data structure
    chart = pattern['charts'][0]
    assert 'data' in chart, "❌ Missing chart data"
    assert len(chart['data']) == 6, f"❌ Expected 6 data points, got {len(chart['data'])}"
    assert chart['data'][0]['name'] == '2019 Revenue', "❌ Incorrect chart data name"
    assert chart['data'][0]['value'] == '10M', "❌ Incorrect chart data value"
    assert chart['data'][0]['unit'] == 'USD', "❌ Incorrect chart data unit"
    
    # Validate figure data structure
    figure = pattern['figures'][0]
    assert 'elements' in figure, "❌ Missing figure elements"
    assert len(figure['elements']) == 5, f"❌ Expected 5 figure elements, got {len(figure['elements'])}"
    assert figure['elements'][0]['name'] == 'CEO', "❌ Incorrect figure element name"
    
    print("✅ Enhanced element analysis test passed!")
    return True

def test_template_block_creation():
    """Test template block creation with enhanced data"""
    print("\n🧪 Testing Enhanced Template Block Creation...")
    
    # Mock bedrock client
    class MockBedrockClient:
        pass
    
    engine = TemplateInferenceEngine(MockBedrockClient())
    
    # Create mock element pattern with enhanced data
    element_pattern = {
        'type': 'charts_graphs',
        'description': 'Revenue and growth metrics visualization showing company performance trends',
        'texts': ['Revenue Growth Chart', 'Performance Metrics'],
        'charts': [{
            'chart_type': 'bar',
            'title': 'Quarterly Performance',
            'description': 'Shows quarterly revenue and profit margins for 2024',
            'data': [
                {'name': 'Q1 Revenue', 'value': '7.2M', 'unit': 'USD'},
                {'name': 'Q1 Profit', 'value': '1.8M', 'unit': 'USD'},
                {'name': 'Q2 Revenue', 'value': '8.1M', 'unit': 'USD'},
                {'name': 'Q2 Profit', 'value': '2.1M', 'unit': 'USD'}
            ],
            'source': 'Finance Team'
        }],
        'figures': [],
        'is_static': False,
        'has_pii': False,
        'pii_types': ['NONE'],
        'sample_element': {
            'category': 'supporting_elements',
            'importance': 'important',
            'position_hint': 'middle'
        }
    }
    
    # Test block creation
    block = engine._create_comprehensive_template_block(
        'metrics', 1, element_pattern, {}, {}, {}
    )
    
    # Validate enhanced block structure
    assert block is not None, "❌ Block creation failed"
    assert 'description' in block, "❌ Missing description in block"
    assert 'chart_data' in block, "❌ Missing chart_data in block"
    assert 'figure_data' in block, "❌ Missing figure_data in block"
    
    assert block['description'] == element_pattern['description'], "❌ Incorrect block description"
    assert block['chart_data'] == element_pattern['charts'][0], "❌ Incorrect chart data"
    assert block['figure_data'] is None, "❌ Figure data should be None"
    
    # Validate chart data in block
    chart_data = block['chart_data']
    assert chart_data['title'] == 'Quarterly Performance', "❌ Incorrect chart title"
    assert len(chart_data['data']) == 4, f"❌ Expected 4 data points, got {len(chart_data['data'])}"
    
    print("✅ Enhanced template block creation test passed!")
    return True

def test_json_serialization():
    """Test JSON serialization of enhanced template"""
    print("\n🧪 Testing Enhanced JSON Serialization...")
    
    # Create mock enhanced template
    enhanced_template = {
        "template_id": "enhanced_master_v1",
        "name": "Enhanced Master Template with Descriptions",
        "pages": [
            {
                "page_type": "metrics",
                "title": "Performance Metrics",
                "blocks": [
                    {
                        "block_id": "metrics_revenue_1",
                        "type": "charts_graphs",
                        "description": "Comprehensive revenue analysis showing growth trends and forecasts",
                        "content_mode": "dynamic",
                        "chart_data": {
                            "chart_type": "line",
                            "title": "Revenue Trend Analysis",
                            "description": "5-year revenue growth with projections",
                            "data": [
                                {"name": "2020", "value": "15M", "unit": "USD"},
                                {"name": "2021", "value": "18M", "unit": "USD"},
                                {"name": "2022", "value": "22M", "unit": "USD"},
                                {"name": "2023", "value": "27M", "unit": "USD"},
                                {"name": "2024", "value": "33M", "unit": "USD"}
                            ]
                        },
                        "figure_data": None
                    },
                    {
                        "block_id": "metrics_org_2",
                        "type": "figures_images",
                        "description": "Visual representation of company organizational structure",
                        "content_mode": "static",
                        "chart_data": None,
                        "figure_data": {
                            "figure_type": "diagram",
                            "title": "Company Structure",
                            "description": "Hierarchical organization chart with key personnel",
                            "elements": [
                                {"name": "Board", "value": "5 Board Members"},
                                {"name": "Executive", "value": "3 C-Level Executives"},
                                {"name": "Management", "value": "12 Department Heads"},
                                {"name": "Staff", "value": "150 Employees"}
                            ]
                        }
                    }
                ]
            }
        ]
    }
    
    # Test JSON serialization
    try:
        json_str = json.dumps(enhanced_template, indent=2, ensure_ascii=False)
        
        # Test deserialization
        parsed_template = json.loads(json_str)
        
        # Validate structure
        assert parsed_template['template_id'] == enhanced_template['template_id'], "❌ Template ID mismatch"
        assert len(parsed_template['pages']) == 1, "❌ Incorrect number of pages"
        
        page = parsed_template['pages'][0]
        assert len(page['blocks']) == 2, "❌ Incorrect number of blocks"
        
        # Validate first block (chart)
        chart_block = page['blocks'][0]
        assert chart_block['description'], "❌ Missing block description"
        assert chart_block['chart_data'], "❌ Missing chart data"
        assert len(chart_block['chart_data']['data']) == 5, "❌ Incorrect chart data length"
        
        # Validate second block (figure)
        figure_block = page['blocks'][1]
        assert figure_block['description'], "❌ Missing figure block description"
        assert figure_block['figure_data'], "❌ Missing figure data"
        assert len(figure_block['figure_data']['elements']) == 4, "❌ Incorrect figure elements length"
        
        print("✅ Enhanced JSON serialization test passed!")
        
        # Save test output
        with open('enhanced_template_test_output.json', 'w', encoding='utf-8') as f:
            f.write(json_str)
        
        print(f"💾 Enhanced template saved to: enhanced_template_test_output.json")
        print(f"📏 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False

def run_enhanced_features_tests():
    """Run all enhanced features tests"""
    print("🚀 Enhanced Features Test Suite")
    print("=" * 50)
    
    tests = [
        ("Enhanced Element Analysis", test_enhanced_element_analysis),
        ("Enhanced Template Block Creation", test_template_block_creation),
        ("Enhanced JSON Serialization", test_json_serialization)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ENHANCED FEATURES TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Results: {passed}/{len(results)} tests passed")
    
    if failed == 0:
        print("\n🎉 ALL ENHANCED FEATURES TESTS PASSED!")
        print("✅ Descriptions and chart/figure enhancements are working correctly.")
        return True
    else:
        print(f"\n⚠️ {failed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = run_enhanced_features_tests()
    exit(0 if success else 1)
