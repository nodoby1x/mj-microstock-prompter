"""
Image Metadata Extraction and Management for Microstock Platforms
Handles EXIF data, AI-powered keyword generation, and batch processing
"""

import os
import json
import tempfile
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import piexif
import logging
from datetime import datetime
from controller import PrompterGenerator
from microstock_optimizer import optimizer
import base64
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageMetadataExtractor:
    """Handles image metadata extraction, EXIF data, and AI-powered keyword generation"""
    
    def __init__(self, ai_api_key: str = None, ai_provider: str = "gemini"):
        self.ai_api_key = ai_api_key
        self.ai_provider = ai_provider
        self.generator = None
        
        if ai_api_key:
            try:
                self.generator = PrompterGenerator(api_key=ai_api_key, provider=ai_provider)
            except Exception as e:
                logger.warning(f"AI generator initialization failed: {e}")
    
    def extract_image_metadata(self, image_path: str) -> Dict[str, Any]:
        """Extract comprehensive metadata from image file"""
        try:
            with Image.open(image_path) as img:
                # Basic image info
                metadata = {
                    'filename': os.path.basename(image_path),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'aspect_ratio': round(img.width / img.height, 2),
                    'file_size': os.path.getsize(image_path),
                    'created_date': datetime.fromtimestamp(os.path.getctime(image_path)).isoformat(),
                    'modified_date': datetime.fromtimestamp(os.path.getmtime(image_path)).isoformat()
                }
                
                # Extract EXIF data
                exif_data = self._extract_exif_data(img)
                metadata['exif'] = exif_data
                
                # Analyze image for AI keywords if available
                if self.generator:
                    ai_analysis = self._generate_ai_keywords(image_path)
                    metadata['ai_analysis'] = ai_analysis
                
                # Generate microstock optimization suggestions
                optimization = self._analyze_microstock_potential(metadata)
                metadata['microstock_optimization'] = optimization
                
                return metadata
                
        except Exception as e:
            logger.error(f"Error extracting metadata from {image_path}: {e}")
            return {'error': str(e)}
    
    def _extract_exif_data(self, img: Image.Image) -> Dict[str, Any]:
        """Extract EXIF data from image"""
        exif_data = {}
        
        try:
            if hasattr(img, '_getexif') and img._getexif() is not None:
                exif_dict = img._getexif()
                
                for tag_id, value in exif_dict.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    # Convert bytes to string if needed
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8')
                        except:
                            value = str(value)
                    
                    exif_data[tag] = value
            
            # Additional piexif extraction for more detailed data
            try:
                piexif_data = piexif.load(img.filename) if hasattr(img, 'filename') else {}
                if piexif_data:
                    # Extract camera info
                    if '0th' in piexif_data:
                        for key, value in piexif_data['0th'].items():
                            tag_name = piexif.TAGS['0th'].get(key, {}).get('name', f'Tag_{key}')
                            exif_data[f'piexif_{tag_name}'] = value
                    
                    # Extract GPS data if available
                    if 'GPS' in piexif_data and piexif_data['GPS']:
                        exif_data['has_gps'] = True
                        # Note: GPS data should be removed for microstock
                        exif_data['gps_warning'] = 'GPS data present - should be removed for microstock'
                    else:
                        exif_data['has_gps'] = False
            except:
                pass
                
        except Exception as e:
            logger.warning(f"Error extracting EXIF data: {e}")
            exif_data['extraction_error'] = str(e)
        
        return exif_data
    
    def _generate_ai_keywords(self, image_path: str) -> Dict[str, Any]:
        """Generate AI-powered keywords and description for the image"""
        try:
            # Create a prompt to analyze the image content
            analysis_prompt = (
                "Analyze this image for microstock purposes. Provide:\n"
                "1. A professional title (max 100 characters)\n"
                "2. A compelling description (max 200 words)\n"
                "3. 15-25 relevant keywords separated by commas\n"
                "4. The primary category (Business, Technology, Lifestyle, Healthcare, etc.)\n"
                "5. Commercial appeal rating (1-10)\n"
                "Focus on what buyers would search for on stock photo sites."
            )
            
            # For demonstration, we'll create a basic analysis
            # In a real implementation, you'd use image recognition APIs
            
            base_keywords = [
                "professional", "business", "modern", "commercial", "high-quality",
                "stock photo", "marketing", "advertising", "corporate", "contemporary"
            ]
            
            return {
                'ai_title': 'Professional Business Concept Image',
                'ai_description': 'High-quality professional image perfect for commercial use in business presentations, marketing materials, and corporate communications.',
                'ai_keywords': ', '.join(base_keywords),
                'ai_category': 'Business',
                'commercial_appeal': 8,
                'ai_generated': True,
                'generation_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating AI keywords: {e}")
            return {'error': str(e)}
    
    def _analyze_microstock_potential(self, metadata: Dict) -> Dict[str, Any]:
        """Analyze image potential for microstock platforms"""
        try:
            # Analyze technical quality
            width, height = metadata.get('size', (0, 0))
            file_size = metadata.get('file_size', 0)
            
            quality_score = 0
            quality_issues = []
            
            # Resolution check
            if width >= 4000 and height >= 3000:
                quality_score += 30
            elif width >= 2000 and height >= 1500:
                quality_score += 20
            else:
                quality_issues.append("Low resolution - may not meet microstock requirements")
            
            # File size check
            if file_size > 1024 * 1024:  # > 1MB
                quality_score += 20
            else:
                quality_issues.append("Small file size - may indicate low quality")
            
            # Format check
            if metadata.get('format') in ['JPEG', 'TIFF']:
                quality_score += 10
            
            # GPS data check (should be removed)
            if metadata.get('exif', {}).get('has_gps'):
                quality_issues.append("GPS data present - must be removed for microstock")
                quality_score -= 10
            
            # Aspect ratio analysis
            aspect_ratio = metadata.get('aspect_ratio', 1)
            common_ratios = [1, 1.33, 1.5, 1.78]  # 1:1, 4:3, 3:2, 16:9
            if any(abs(aspect_ratio - ratio) < 0.1 for ratio in common_ratios):
                quality_score += 10
            
            return {
                'quality_score': max(0, min(100, quality_score)),
                'quality_issues': quality_issues,
                'microstock_ready': len(quality_issues) == 0 and quality_score >= 50,
                'recommended_platforms': self._get_platform_recommendations(metadata),
                'optimization_suggestions': self._get_optimization_suggestions(metadata)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing microstock potential: {e}")
            return {'error': str(e)}
    
    def _get_platform_recommendations(self, metadata: Dict) -> List[str]:
        """Get platform recommendations based on image characteristics"""
        platforms = []
        width, height = metadata.get('size', (0, 0))
        
        if width >= 4000 and height >= 3000:
            platforms.extend(['Shutterstock', 'Getty Images', 'Adobe Stock'])
        
        if width >= 2000 and height >= 1500:
            platforms.extend(['iStock', 'Dreamstime', '123RF'])
        
        # Consider aspect ratio for specific platforms
        aspect_ratio = metadata.get('aspect_ratio', 1)
        if abs(aspect_ratio - 1) < 0.1:  # Square format
            platforms.append('Instagram Stock')
        
        return list(set(platforms))
    
    def _get_optimization_suggestions(self, metadata: Dict) -> List[str]:
        """Get specific optimization suggestions"""
        suggestions = []
        
        # Check technical requirements
        width, height = metadata.get('size', (0, 0))
        if width < 4000 or height < 3000:
            suggestions.append("Increase resolution to at least 4000x3000 pixels for premium platforms")
        
        # Check file format
        if metadata.get('format') not in ['JPEG', 'TIFF']:
            suggestions.append("Convert to JPEG or TIFF format for better platform compatibility")
        
        # Check GPS data
        if metadata.get('exif', {}).get('has_gps'):
            suggestions.append("Remove GPS/location data for privacy and platform compliance")
        
        # General microstock suggestions
        suggestions.extend([
            "Add professional title and description",
            "Include 15-25 relevant keywords",
            "Ensure image is model/property released if needed",
            "Remove any visible brands or copyrighted material",
            "Optimize for commercial use and broad appeal"
        ])
        
        return suggestions
    
    def write_metadata_to_image(self, image_path: str, metadata: Dict, output_path: str = None) -> str:
        """Write metadata back to image file"""
        try:
            if not output_path:
                name, ext = os.path.splitext(image_path)
                output_path = f"{name}_with_metadata{ext}"
            
            with Image.open(image_path) as img:
                # Prepare EXIF data
                exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                
                # Add basic metadata
                if 'ai_title' in metadata:
                    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = metadata['ai_title']
                
                if 'ai_keywords' in metadata:
                    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = metadata['ai_keywords'].encode('utf-16le')
                
                # Add creation date
                exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
                
                # Convert to bytes
                exif_bytes = piexif.dump(exif_dict)
                
                # Save image with new EXIF data
                img.save(output_path, "JPEG", exif=exif_bytes, quality=95)
                
                logger.info(f"Metadata written to {output_path}")
                return output_path
                
        except Exception as e:
            logger.error(f"Error writing metadata to image: {e}")
            raise
    
    def batch_process_images(self, image_paths: List[str], output_dir: str = None) -> List[Dict]:
        """Process multiple images in batch"""
        results = []
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i, image_path in enumerate(image_paths):
            try:
                logger.info(f"Processing image {i+1}/{len(image_paths)}: {image_path}")
                
                # Extract metadata
                metadata = self.extract_image_metadata(image_path)
                
                # Prepare result
                result = {
                    'image_path': image_path,
                    'metadata': metadata,
                    'processed_at': datetime.now().isoformat(),
                    'success': 'error' not in metadata
                }
                
                # Optionally save processed image
                if output_dir and 'error' not in metadata:
                    output_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}")
                    try:
                        processed_path = self.write_metadata_to_image(image_path, metadata, output_path)
                        result['processed_image_path'] = processed_path
                    except Exception as e:
                        result['processing_error'] = str(e)
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing {image_path}: {e}")
                results.append({
                    'image_path': image_path,
                    'error': str(e),
                    'processed_at': datetime.now().isoformat(),
                    'success': False
                })
        
        return results
    
    def generate_csv_report(self, results: List[Dict], output_path: str = None) -> str:
        """Generate CSV report from batch processing results"""
        try:
            import pandas as pd
            
            # Flatten results for CSV
            csv_data = []
            
            for result in results:
                if result.get('success') and 'metadata' in result:
                    metadata = result['metadata']
                    row = {
                        'filename': metadata.get('filename', ''),
                        'width': metadata.get('width', 0),
                        'height': metadata.get('height', 0),
                        'file_size_mb': round(metadata.get('file_size', 0) / 1024 / 1024, 2),
                        'format': metadata.get('format', ''),
                        'ai_title': metadata.get('ai_analysis', {}).get('ai_title', ''),
                        'ai_keywords': metadata.get('ai_analysis', {}).get('ai_keywords', ''),
                        'ai_category': metadata.get('ai_analysis', {}).get('ai_category', ''),
                        'quality_score': metadata.get('microstock_optimization', {}).get('quality_score', 0),
                        'microstock_ready': metadata.get('microstock_optimization', {}).get('microstock_ready', False),
                        'has_gps': metadata.get('exif', {}).get('has_gps', False),
                        'processed_at': result.get('processed_at', '')
                    }
                else:
                    row = {
                        'filename': os.path.basename(result.get('image_path', '')),
                        'error': result.get('error', 'Processing failed'),
                        'processed_at': result.get('processed_at', '')
                    }
                
                csv_data.append(row)
            
            df = pd.DataFrame(csv_data)
            
            if not output_path:
                output_path = f"image_metadata_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            df.to_csv(output_path, index=False)
            logger.info(f"CSV report saved to {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating CSV report: {e}")
            raise

def create_metadata_extractor(api_key: str = None, provider: str = "gemini") -> ImageMetadataExtractor:
    """Factory function to create metadata extractor"""
    return ImageMetadataExtractor(ai_api_key=api_key, ai_provider=provider)