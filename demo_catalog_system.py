#!/usr/bin/env python3
"""
Demo Script: Master Template Generation with Catalog Integration
Shows how the system works with mock data
"""

import json
from catalog_integration import CatalogIntegration

def demo_catalog_system():
    """Demonstrate the catalog integration system"""
    
    print("🎯 Master Template Generation System Demo")
    print("=" * 50)
    
    # Initialize catalog
    print("\n📋 Loading Master Catalog...")
    catalog = CatalogIntegration()
    
    summary = catalog.get_catalog_summary()
    print(f"✅ Loaded: {summary['catalog_name']}")
    print(f"   • Version: {summary['version']}")
    print(f"   • Sections: {summary['total_sections']}")
    print(f"   • Elements: {summary['total_elements']}")
    
    # Show sample elements
    print(f"\n📚 Sample Elements from Catalog:")
    sample_elements = list(catalog.element_registry.values())[:5]
    for elem in sample_elements:
        print(f"   • {elem['field_id']}: {elem['label']} ({elem['data_type']})")
    
    # Demo element detection
    print(f"\n🔍 Simulating Document Analysis...")
    
    mock_detected_elements = [
        {'element_id': 'e1', 'type': 'title', 'text': 'Company Profile 2024', 'importance': 'critical'},
        {'element_id': 'e2', 'type': 'subtitle', 'text': 'Annual Overview', 'importance': 'important'},
        {'element_id': 'e3', 'type': 'authors', 'text': 'Acme Corporation', 'importance': 'important'},
        {'element_id': 'e4', 'type': 'executive_summary_text', 'text': 'We are a leading technology company...', 'importance': 'critical'},
        {'element_id': 'e5', 'type': 'key_recommendations', 'text': 'Focus on digital transformation...', 'importance': 'critical'},
        {'element_id': 'e6', 'type': 'contact_email', 'text': 'info@acme.com', 'importance': 'optional'},
        {'element_id': 'e7', 'type': 'custom_metric', 'text': '95% customer satisfaction', 'importance': 'important'}  # Not in catalog
    ]
    
    print(f"   📄 Detected {len(mock_detected_elements)} elements from documents")
    
    # Map elements to catalog
    print(f"\n🔗 Mapping Elements to Catalog...")
    mapped_elements = catalog.map_detected_elements(mock_detected_elements)
    
    mapped_count = len([e for e in mapped_elements if e['mapping_status'] == 'mapped'])
    unmapped_count = len([e for e in mapped_elements if e['mapping_status'] == 'unmapped'])
    
    print(f"   ✅ Mapped to catalog: {mapped_count}")
    print(f"   ⚠️ Custom elements: {unmapped_count}")
    
    # Show mapping details
    print(f"\n📊 Element Mapping Details:")
    for mapped_elem in mapped_elements:
        detected = mapped_elem['detected_element']
        status_icon = "✅" if mapped_elem['mapping_status'] == 'mapped' else "⚠️"
        field_schema = mapped_elem['field_schema']
        
        print(f"   {status_icon} {detected['type']} → {field_schema['label']} ({field_schema['data_type']})")
        if field_schema['pii_type'] != 'NONE':
            print(f"      🔒 PII Type: {field_schema['pii_type']}")
    
    # Coverage analysis
    print(f"\n📈 Coverage Analysis...")
    coverage = catalog.analyze_catalog_coverage(mock_detected_elements)
    
    print(f"   • Total Elements Detected: {coverage['total_elements_detected']}")
    print(f"   • Mapped to Catalog: {coverage['elements_mapped_to_catalog']}")
    print(f"   • Coverage Percentage: {coverage['coverage_percentage']}%")
    
    if coverage['unmapped_elements']:
        print(f"   • Unmapped Elements: {', '.join(coverage['unmapped_elements'])}")
    
    # Generate template
    print(f"\n🧠 Generating Master Template...")
    
    # Create mock element frequency data
    element_frequency = {}
    for mapped_elem in mapped_elements:
        field_id = mapped_elem['field_schema']['field_id']
        element_frequency[field_id] = {
            'total_count': 1,
            'document_count': 1,
            'document_percentage': 100.0,
            'is_static': False
        }
    
    template = catalog.generate_catalog_based_template(mapped_elements, element_frequency)
    
    print(f"   ✅ Generated: {template['name']}")
    print(f"   • Template ID: {template['template_id']}")
    print(f"   • Based on Catalog: {template['based_on_catalog']}")
    print(f"   • Elements Used: {template['catalog_integration']['elements_used']}")
    
    # Show common elements
    print(f"\n🎯 Common Elements in Template:")
    for elem in template['common_elements'][:5]:
        print(f"   • {elem['element_type']} ({elem['category']})")
        print(f"     - Frequency: {elem['frequency_percentage']}%")
        print(f"     - Mapping: {elem['mapping_status']}")
        if elem['catalog_definition']:
            print(f"     - Description: {elem['catalog_definition']['description'][:50]}...")
    
    # Save demo output
    output_file = 'demo_template_output.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Demo template saved to: {output_file}")
    
    print(f"\n🎉 Demo Complete!")
    print(f"   The system successfully:")
    print(f"   ✅ Loaded comprehensive catalog with {summary['total_elements']} elements")
    print(f"   ✅ Mapped {coverage['coverage_percentage']}% of detected elements")
    print(f"   ✅ Generated structured master template")
    print(f"   ✅ Handled PII detection and custom elements")
    
    return template

if __name__ == "__main__":
    demo_catalog_system()
