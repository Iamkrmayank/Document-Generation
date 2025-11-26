import boto3
import json
import streamlit as st
from typing import Dict, Any, Optional, List
import logging
from catalog_integration import CatalogIntegration

class BedrockClient:
    def __init__(self, region: str = "eu-west-1"):
        """Initialize Bedrock client for Claude Sonnet 4.5 with catalog integration"""
        self.region = region
        self.model_id = "eu.anthropic.claude-sonnet-4-5-20250929-v1:0"
        
        # Initialize catalog integration
        self.catalog = CatalogIntegration()
        
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=region
            )
        except Exception as e:
            st.error(f"Failed to initialize AWS Bedrock client: {str(e)}")
            st.error("Please ensure AWS credentials are configured via environment variables")
            raise
    
    def _call_claude(self, system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> Optional[str]:
        """Call Claude via Bedrock with proper message formatting"""
        
        try:
            # Prepare the request body
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "temperature": 0.1,  # Low temperature for consistent structured output
                "top_p": 0.9
            }
            
            # Call Bedrock
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                st.error("Unexpected response format from Claude")
                return None
                
        except Exception as e:
            st.error(f"Error calling Claude: {str(e)}")
            return None
    
    def extract_page_structure(self, page_content: str, doc_id: str, page_index: int) -> Optional[Dict[str, Any]]:
        """Extract comprehensive structured JSON representation using master catalog"""
        
        # Get available elements from catalog
        catalog_elements = self.catalog.get_element_types_for_prompt()
        
        system_prompt = f"""You are an expert document structure analyzer using a comprehensive master catalog. Your task is to extract the complete structure of a document page using ONLY elements defined in the master catalog.

{catalog_elements}

IMPORTANT INSTRUCTIONS:
1. ONLY use element types (field_id values) that exist in the catalog above
2. Match detected elements to the exact field_id from the catalog
3. Use the correct category for each element as shown in the catalog
4. Detect PII according to the catalog definitions
5. Generate meaningful descriptions explaining what each element contains
6. For charts/figures, extract structured data as name-value pairs

For each element detected, return:
{{
  "element_id": "e1",
  "type": "exact_field_id_from_catalog",
  "category": "document_identity_and_metadata|front_matter|introduction_section|main_body_core_content|supporting_elements|analysis_and_findings|recommendations_solutions|conclusion_closing_section|end_matter",
  "importance": "critical|important|optional|supplementary",
  "text": "actual content from document",
  "description": "Clear explanation of what this element contains and its purpose",
  "items": ["for lists"],
  "table": {{"headers": ["col1"], "rows": [["val1"]]}},
  "chart": {{
    "chart_type": "bar|line|pie|scatter|area",
    "title": "Chart Title",
    "description": "What this chart shows and its significance",
    "data": [
      {{"name": "Revenue", "value": "50M", "unit": "USD"}},
      {{"name": "Growth", "value": "25", "unit": "%"}},
      {{"name": "Customers", "value": "10000", "unit": "count"}}
    ],
    "source": "Data source if mentioned"
  }},
  "figure": {{
    "figure_type": "diagram|image|infographic|logo",
    "title": "Figure Title",
    "description": "What this figure shows and its purpose",
    "elements": [
      {{"name": "Element1", "value": "Description1"}},
      {{"name": "Element2", "value": "Description2"}}
    ]
  }},
  "position_hint": "top|middle|bottom|header|footer",
  "pii_type": "NONE|ORG_NAME|PERSON_NAME|EMAIL|PHONE|ADDRESS|URL|DATE"
}}

DESCRIPTION EXAMPLES:
- title: "Main document heading that identifies the company profile"
- executive_summary_text: "Brief overview summarizing key company highlights and market position"
- contact_email: "Primary business email for customer inquiries and partnerships"
- charts_graphs: "Visual representation showing company performance metrics over time"
- organization_logo: "Company brand logo used for visual identification"

CHART DATA EXAMPLES:
- Revenue chart: {{"name": "Q1 Revenue", "value": "2.5M", "unit": "USD"}}
- Growth metrics: {{"name": "YoY Growth", "value": "15", "unit": "%"}}
- Employee count: {{"name": "Total Employees", "value": "250", "unit": "people"}}

FIGURE EXAMPLES:
- Company structure: {{"name": "CEO", "value": "John Smith"}}, {{"name": "CTO", "value": "Jane Doe"}}
- Process flow: {{"name": "Step 1", "value": "Data Collection"}}, {{"name": "Step 2", "value": "Analysis"}}

Return ONLY valid JSON with no additional commentary."""

        user_prompt = f"""Analyze this page content and extract its comprehensive structure:

PAGE CONTENT:
{page_content}

Return a JSON object with this exact structure:
{{
  "doc_id": "{doc_id}",
  "page_index": {page_index},
  "page_role": "cover|front_matter|introduction|main_content|analysis|recommendations|conclusion|end_matter",
  "elements": [
    {{
      "element_id": "e1",
      "type": "title|subtitle|author|organization|version_number|document_id|date_created|last_updated|confidentiality_level|cover_page|preface|acknowledgements|table_of_contents|list_of_figures|list_of_tables|executive_summary|abstract|introduction|purpose|scope|background|problem_statement|audience|assumptions|heading|subheading|paragraph|bullet_list|number_list|definition|case_study|procedure|workflow|diagram|table|chart|screenshot|callout|note|tip|warning|figure|image|flowchart|data_highlight|equation|code_block|footnote|hyperlink|data_analysis|findings|observations|patterns|interpretation|comparison|limitation|key_recommendations|action_plan|roadmap|strategy|best_practices|implementation_steps|summary|final_conclusion|insights|way_forward|closing_statement|glossary|references|bibliography|appendix|index|contact_information",
      "category": "metadata|front_matter|main_body|supporting|analysis|recommendations|conclusion|end_matter",
      "importance": "critical|important|optional|supplementary",
      "text": "text content for text-like elements",
      "items": ["item1", "item2"],
      "table": {{
        "headers": ["col1", "col2"],
        "rows": [["val1", "val2"]]
      }},
      "chart": {{
        "chart_type": "pie|bar|line|scatter",
        "labels": ["label1", "label2"],
        "values": [10, 20],
        "description": "chart description"
      }},
      "metadata": {{
        "author": "author name if applicable",
        "date": "date if applicable",
        "version": "version if applicable"
      }},
      "position_hint": "top|middle|bottom|header|footer",
      "pii_type": "NONE|ORG_NAME|PERSON_NAME|EMAIL|PHONE|ADDRESS|URL|DATE"
    }}
  ]
}}

Guidelines:
- Identify the page_role based on content (cover, introduction, main_content, etc.)
- Use comprehensive element types from the provided list
- Categorize each element (metadata, front_matter, main_body, etc.)
- Set importance level (critical for titles/key content, supplementary for footnotes)
- Use "text" field for text-like elements
- Use "items" array for lists
- Use "table" object for tabular data
- Use "chart" object for charts/graphs with description
- Use "metadata" object for document metadata elements
- Set position_hint for layout information
- Set pii_type for any personally identifiable information
- Generate meaningful element_id values (e1, e2, etc.)
- Include ALL visible content elements, no matter how small"""

        response = self._call_claude(system_prompt, user_prompt)
        
        if response:
            try:
                # Clean response and parse JSON
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]
                
                return json.loads(response)
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse JSON response for {doc_id} page {page_index}: {str(e)}")
                st.error(f"Raw response: {response[:500]}...")
                return None
        
        return None
    
    def suggest_page_types(self, page_summaries: list) -> Optional[Dict[str, Any]]:
        """Use Claude to suggest page type classifications"""
        
        system_prompt = """You are a document structure analyst. Given summaries of pages from multiple company profile documents, classify them into logical page types and suggest normalized names."""
        
        summaries_text = "\n".join([
            f"Page {i+1}: {summary}" for i, summary in enumerate(page_summaries)
        ])
        
        user_prompt = f"""Analyze these page summaries from company profile documents and suggest page type classifications:

{summaries_text}

Return JSON with suggested page types:
{{
  "page_types": [
    {{
      "page_type": "cover",
      "description": "Cover page with company name and logo",
      "typical_elements": ["company_name", "logo", "tagline"]
    }},
    {{
      "page_type": "about",
      "description": "About the company section",
      "typical_elements": ["heading", "company_description", "highlights"]
    }}
  ]
}}"""
        
        response = self._call_claude(system_prompt, user_prompt)
        
        if response:
            try:
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]
                
                return json.loads(response)
            except json.JSONDecodeError:
                return None
        
        return None
    
    def get_catalog_summary(self) -> Dict[str, Any]:
        """Get summary of the master catalog"""
        return self.catalog.get_catalog_summary()
    
    def analyze_catalog_coverage(self, all_page_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how well detected elements match the catalog"""
        
        all_detected_elements = []
        for page_data in all_page_data:
            all_detected_elements.extend(page_data.get('elements', []))
        
        return self.catalog.analyze_catalog_coverage(all_detected_elements)
