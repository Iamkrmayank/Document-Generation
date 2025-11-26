#!/usr/bin/env python3
"""
Catalog Integration Module for Master Template System
Integrates master_template.json with document analysis
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

class CatalogIntegration:
    def __init__(self, catalog_path: str = "master_template.json"):
        """Initialize catalog integration"""
        self.catalog_path = catalog_path
        self.master_catalog = self._load_catalog()
        self.element_registry = self._build_element_registry()
    
    def _load_catalog(self) -> Dict[str, Any]:
        """Load master template catalog"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
            print(f"✅ Loaded master catalog: {catalog.get('name', 'Unknown')}")
            return catalog
        except FileNotFoundError:
            print(f"❌ Master catalog not found: {self.catalog_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in catalog: {e}")
            return {}
    
    def _build_element_registry(self) -> Dict[str, Dict[str, Any]]:
        """Build registry of all available elements from catalog"""
        registry = {}
        
        if not self.master_catalog:
            return registry
        
        sections = self.master_catalog.get('sections', {})
        
        for section_name, section_data in sections.items():
            self._extract_elements_from_section(section_data, section_name, registry)
        
        print(f"📋 Built element registry with {len(registry)} elements")
        return registry
    
    def _extract_elements_from_section(self, section_data: Dict, section_name: str, registry: Dict, parent_key: str = ""):
        """Recursively extract elements from section"""
        
        for key, value in section_data.items():
            if isinstance(value, dict):
                if 'field_id' in value:
                    # This is an element definition
                    field_id = value['field_id']
                    registry[field_id] = {
                        'field_id': field_id,
                        'label': value.get('label', key.replace('_', ' ').title()),
                        'description': value.get('description', ''),
                        'data_type': value.get('data_type', 'string'),
                        'required': value.get('required', False),
                        'pii_type': value.get('pii_type', 'NONE'),
                        'category': section_name,
                        'parent_key': parent_key,
                        'schema': value.get('schema', {})
                    }
                else:
                    # Nested structure, recurse
                    nested_parent = f"{parent_key}.{key}" if parent_key else key
                    self._extract_elements_from_section(value, section_name, registry, nested_parent)
    
    def get_available_elements(self) -> List[Dict[str, Any]]:
        """Get list of all available elements for Claude prompt"""
        return list(self.element_registry.values())
    
    def get_element_types_for_prompt(self) -> str:
        """Get formatted element types for Claude prompt"""
        elements_by_category = defaultdict(list)
        
        for element in self.element_registry.values():
            category = element['category']
            elements_by_category[category].append(element['field_id'])
        
        prompt_text = "AVAILABLE ELEMENT TYPES FROM MASTER CATALOG:\n\n"
        
        for category, elements in elements_by_category.items():
            category_name = category.replace('_', ' ').title()
            prompt_text += f"**{category_name}:**\n"
            for element in sorted(elements):
                element_def = self.element_registry[element]
                prompt_text += f"  - {element}: {element_def['label']} ({element_def['data_type']})\n"
            prompt_text += "\n"
        
        return prompt_text
    
    def find_element_definition(self, field_id: str) -> Optional[Dict[str, Any]]:
        """Find element definition by field_id"""
        return self.element_registry.get(field_id)
    
    def map_detected_elements(self, detected_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map detected elements to catalog definitions"""
        mapped_elements = []
        
        for element in detected_elements:
            element_type = element.get('type', '')
            catalog_def = self.find_element_definition(element_type)
            
            if catalog_def:
                mapped_elements.append({
                    'detected_element': element,
                    'catalog_definition': catalog_def,
                    'mapping_status': 'mapped',
                    'field_schema': {
                        'field_id': catalog_def['field_id'],
                        'label': catalog_def['label'],
                        'data_type': catalog_def['data_type'],
                        'required': catalog_def['required'],
                        'pii_type': catalog_def['pii_type'],
                        'description': catalog_def['description'],
                        'category': catalog_def['category']
                    }
                })
            else:
                # Element not found in catalog
                mapped_elements.append({
                    'detected_element': element,
                    'catalog_definition': None,
                    'mapping_status': 'unmapped',
                    'field_schema': {
                        'field_id': f"custom_{element_type}",
                        'label': element_type.replace('_', ' ').title(),
                        'data_type': 'string',
                        'required': False,
                        'pii_type': element.get('pii_type', 'NONE'),
                        'description': f"Custom element: {element_type}",
                        'category': 'custom'
                    }
                })
        
        return mapped_elements
    
    def analyze_catalog_coverage(self, detected_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how well detected elements match catalog"""
        
        total_detected = len(detected_elements)
        mapped_count = 0
        unmapped_elements = []
        mapped_elements = []
        
        for element in detected_elements:
            element_type = element.get('type', '')
            if self.find_element_definition(element_type):
                mapped_count += 1
                mapped_elements.append(element_type)
            else:
                unmapped_elements.append(element_type)
        
        coverage_percentage = (mapped_count / total_detected * 100) if total_detected > 0 else 0
        
        return {
            'total_elements_detected': total_detected,
            'elements_mapped_to_catalog': mapped_count,
            'elements_unmapped': len(unmapped_elements),
            'coverage_percentage': round(coverage_percentage, 1),
            'mapped_elements': mapped_elements,
            'unmapped_elements': unmapped_elements,
            'catalog_total_elements': len(self.element_registry)
        }
    
    def generate_catalog_based_template(self, mapped_elements: List[Dict[str, Any]], 
                                      element_frequency: Dict[str, Any]) -> Dict[str, Any]:
        """Generate template using catalog definitions"""
        
        template = {
            "template_id": "catalog_based_master_v1",
            "name": "Catalog-Based Master Template",
            "description": "Master template generated using comprehensive document elements catalog",
            "based_on_catalog": self.master_catalog.get('template_id', 'unknown'),
            "catalog_version": self.master_catalog.get('version', '1.0'),
            "created_date": self.master_catalog.get('created_date', '2024-11-26'),
            "catalog_integration": {
                "catalog_name": self.master_catalog.get('name', 'Unknown'),
                "total_catalog_elements": len(self.element_registry),
                "elements_used": 0,
                "coverage_analysis": {}
            },
            "common_elements": [],
            "page_templates": []
        }
        
        # Build common elements using catalog definitions
        common_elements = []
        
        for element_key, stats in element_frequency.items():
            if stats.get('frequency_percentage', 0) >= 50:  # Common elements
                
                # Find corresponding mapped element
                for mapped_elem in mapped_elements:
                    detected = mapped_elem['detected_element']
                    if detected.get('type') == element_key.split('_')[0]:
                        
                        catalog_def = mapped_elem['catalog_definition']
                        field_schema = mapped_elem['field_schema']
                        
                        common_elements.append({
                            'element_type': field_schema['field_id'],
                            'category': field_schema['category'],
                            'frequency_percentage': stats['frequency_percentage'],
                            'appears_in_documents': stats.get('document_count', 0),
                            'mapping_status': mapped_elem['mapping_status'],
                            'catalog_definition': catalog_def,
                            'field_schema': field_schema,
                            'content_analysis': {
                                'is_static': stats.get('is_static', False),
                                'sample_content': stats.get('content_samples', [])[:3],
                                'pii_detected': list(stats.get('pii_types', set()))
                            }
                        })
                        break
        
        template['common_elements'] = common_elements
        template['catalog_integration']['elements_used'] = len(common_elements)
        
        return template
    
    def get_catalog_summary(self) -> Dict[str, Any]:
        """Get summary of catalog structure"""
        
        if not self.master_catalog:
            return {}
        
        sections = self.master_catalog.get('sections', {})
        section_summary = {}
        
        for section_name, section_data in sections.items():
            element_count = self._count_elements_in_section(section_data)
            section_summary[section_name] = {
                'name': section_name.replace('_', ' ').title(),
                'element_count': element_count
            }
        
        return {
            'catalog_id': self.master_catalog.get('template_id', 'unknown'),
            'catalog_name': self.master_catalog.get('name', 'Unknown'),
            'version': self.master_catalog.get('version', '1.0'),
            'total_sections': len(sections),
            'total_elements': len(self.element_registry),
            'sections': section_summary
        }
    
    def _count_elements_in_section(self, section_data: Dict) -> int:
        """Count elements in a section"""
        count = 0
        
        for key, value in section_data.items():
            if isinstance(value, dict):
                if 'field_id' in value:
                    count += 1
                else:
                    count += self._count_elements_in_section(value)
        
        return count
