<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multimodal RAG System - Technical Overview</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --accent-color: #3b82f6;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-accent: #eff6ff;
            --border-color: #e5e7eb;
            --success-color: #059669;
            --warning-color: #d97706;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }

        .header-content {
            position: relative;
            z-index: 1;
        }

        h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ffffff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            font-size: 1.25rem;
            font-weight: 300;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }

        nav {
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
            background-color: rgba(248, 250, 252, 0.9);
        }

        .nav-container {
            display: flex;
            justify-content: center;
            padding: 1rem 0;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-secondary);
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
        }

        .nav-links a:hover {
            color: var(--primary-color);
            background-color: var(--bg-accent);
        }

        main {
            padding: 3rem 0;
        }

        .section {
            margin-bottom: 4rem;
        }

        .section-header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .section-title {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
            position: relative;
            display: inline-block;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            border-radius: 2px;
        }

        .section-description {
            font-size: 1.125rem;
            color: var(--text-secondary);
            max-width: 800px;
            margin: 0 auto;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .card {
            background-color: var(--bg-primary);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        .card-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            border-radius: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            color: white;
            font-size: 1.5rem;
        }

        .card-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .card-content {
            color: var(--text-secondary);
            line-height: 1.7;
        }

        .code-block {
            background-color: #1e293b;
            color: #e2e8f0;
            padding: 1.5rem;
            border-radius: 0.5rem;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.875rem;
            line-height: 1.6;
            overflow-x: auto;
            margin: 1rem 0;
            border-left: 4px solid var(--primary-color);
        }

        .highlight {
            background: linear-gradient(120deg, var(--bg-accent) 0%, var(--bg-accent) 100%);
            padding: 2rem;
            border-radius: 1rem;
            border-left: 4px solid var(--primary-color);
            margin: 2rem 0;
        }

        .feature-list {
            list-style: none;
            margin: 1rem 0;
        }

        .feature-list li {
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
            color: var(--text-secondary);
        }

        .feature-list li::before {
            content: '✓';
            color: var(--success-color);
            font-weight: bold;
            margin-right: 0.75rem;
            font-size: 1.125rem;
        }

        .architecture-diagram {
            background-color: var(--bg-secondary);
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
            border: 2px dashed var(--border-color);
        }

        .flow-step {
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            margin: 0.25rem;
            font-weight: 500;
            font-size: 0.875rem;
        }

        .arrow {
            color: var(--text-secondary);
            font-size: 1.5rem;
            margin: 0 1rem;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .metric-card {
            text-align: center;
            padding: 1.5rem;
            background: linear-gradient(135deg, var(--bg-accent), var(--bg-secondary));
            border-radius: 1rem;
            border: 1px solid var(--border-color);
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-color);
            display: block;
        }

        .metric-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
        }

        footer {
            background-color: var(--text-primary);
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 4rem;
        }

        .scroll-indicator {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            z-index: 1000;
            transition: width 0.3s ease;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            .nav-links {
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .card-grid {
                grid-template-columns: 1fr;
            }
            
            .section-title {
                font-size: 2rem;
            }
        }

        .tab-container {
            margin: 2rem 0;
        }

        .tab-buttons {
            display: flex;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1.5rem;
        }

        .tab-button {
            background: none;
            border: none;
            padding: 1rem 1.5rem;
            cursor: pointer;
            font-weight: 500;
            color: var(--text-secondary);
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .tab-button.active {
            color: var(--primary-color);
            border-bottom-color: var(--primary-color);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="scroll-indicator"></div>
    
    <header>
        <div class="container">
            <div class="header-content">
                <h1>Multimodal RAG System</h1>
                <p class="subtitle">Advanced retrieval architecture combining CLIP embeddings, document chunking strategies, and agentic workflows for intelligent information retrieval</p>
            </div>
        </div>
    </header>

    <nav>
        <div class="container">
            <div class="nav-container">
                <ul class="nav-links">
                    <li><a href="#retrieval">Multimodal Retrieval</a></li>
                    <li><a href="#chunking">Document Chunking</a></li>
                    <li><a href="#evaluation">RAG Evaluation</a></li>
                    <li><a href="#agentic">Agentic Architecture</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <!-- Multimodal Retrieval Section -->
            <section id="retrieval" class="section">
                <div class="section-header">
                    <h2 class="section-title">Multimodal Retrieval System</h2>
                    <p class="section-description">
                        Our system leverages CLIP embeddings to enable cross-modal search between images and text, 
                        creating a unified embedding space for comprehensive product retrieval.
                    </p>
                </div>

                <div class="card-grid">
                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-image"></i>
                        </div>
                        <h3 class="card-title">Image Processing</h3>
                        <div class="card-content">
                            <p>Images are stored as base64 encoded strings and processed through CLIP's vision encoder:</p>
                            <div class="code-block">// Image embedding process
image_data = base64.b64decode(base64_string)
image = Image.open(BytesIO(image_data))
inputs = processor(images=image, return_tensors="pt")
embedding = model.get_image_features(**inputs)</div>
                            <ul class="feature-list">
                                <li>Base64 encoding for storage efficiency</li>
                                <li>PIL Image processing pipeline</li>
                                <li>CLIP vision transformer embeddings</li>
                                <li>GPU acceleration when available</li>
                            </ul>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-font"></i>
                        </div>
                        <h3 class="card-title">Text Processing</h3>
                        <div class="card-content">
                            <p>Text content is tokenized and embedded using CLIP's text encoder:</p>
                            <div class="code-block">// Text embedding process
text_inputs = processor(
    text=text, 
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=77
)
embedding = model.get_text_features(**text_inputs)</div>
                            <ul class="feature-list">
                                <li>Maximum 77 token limit</li>
                                <li>Automatic padding and truncation</li>
                                <li>Shared embedding space with images</li>
                                <li>Cross-modal semantic similarity</li>
                            </ul>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-database"></i>
                        </div>
                        <h3 class="card-title">Vector Storage</h3>
                        <div class="card-content">
                            <p>ChromaDB stores embeddings with metadata for efficient retrieval:</p>
                            <div class="code-block">// Storage differentiation
images = [doc for doc in documents 
         if doc.metadata.get("_type") == 'image']
texts = [doc for doc in documents 
        if doc.metadata.get("_type") != 'image']</div>
                            <ul class="feature-list">
                                <li>Separate handling for images and text</li>
                                <li>Metadata-driven type classification</li>
                                <li>Efficient similarity search</li>
                                <li>Parent-child document relationships</li>
                            </ul>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-search"></i>
                        </div>
                        <h3 class="card-title">Retrieval Process</h3>
                        <div class="card-content">
                            <p>ParentDocumentRetriever enables sophisticated search patterns:</p>
                            <div class="architecture-diagram">
                                <div class="flow-step">Query Input</div>
                                <span class="arrow">→</span>
                                <div class="flow-step">CLIP Embedding</div>
                                <span class="arrow">→</span>
                                <div class="flow-step">Vector Search</div>
                                <span class="arrow">→</span>
                                <div class="flow-step">Parent Document</div>
                                <span class="arrow">→</span>
                                <div class="flow-step">Results (k=10)</div>
                            </div>
                            <ul class="feature-list">
                                <li>Cross-modal query capabilities</li>
                                <li>Context-aware parent retrieval</li>
                                <li>Configurable result count</li>
                                <li>Similarity-based ranking</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="highlight">
                    <h3>Key Architecture Benefits</h3>
                    <p>The multimodal approach enables powerful search scenarios: find products by describing style ("bohemian summer dress"), 
                    search images with color terms ("bright red accessories"), or locate items by occasion ("formal evening wear"). 
                    The shared CLIP embedding space ensures semantic consistency across modalities.</p>
                </div>
            </section>

            <!-- Document Chunking Section -->
            <section id="chunking" class="section">
                <div class="section-header">
                    <h2 class="section-title">Document Chunking Strategies</h2>
                    <p class="section-description">
                        Intelligent document segmentation optimizes retrieval accuracy by creating semantically meaningful 
                        chunks tailored to product data structures and search patterns.
                    </p>
                </div>

                <div class="tab-container">
                    <div class="tab-buttons">
                        <button class="tab-button active" onclick="switchTab(event, 'product-chunking')">Product-Based Chunking</button>
                        <button class="tab-button" onclick="switchTab(event, 'semantic-chunking')">Semantic Strategies</button>
                        <button class="tab-button" onclick="switchTab(event, 'optimization')">Optimization Techniques</button>
                    </div>

                    <div id="product-chunking" class="tab-content active">
                        <div class="card-grid">
                            <div class="card">
                                <div class="card-icon">
                                    <i class="fas fa-puzzle-piece"></i>
                                </div>
                                <h3 class="card-title">Field-Based Splitting</h3>
                                <div class="card-content">
                                    <p>ProductDocumentSplitter creates targeted chunks for each product attribute:</p>
                                    <div class="code-block">// Product field extraction
docs.append(Document(
    page_content=color_text,
    metadata=self.update_metadata(metadata, 
                                field='color', 
                                _type='text')
))

style_text = '\n'.join(product['style']['styles'])
docs.append(Document(
    page_content=style_text,
    metadata=self.update_metadata(metadata,
                                field='style', 
                                _type='text')
))</div>
                                    <ul class="feature-list">
                                        <li>Color descriptions and attributes</li>
                                        <li>Style categories and details</li>
                                        <li>Seasonal and weather suitability</li>
                                        <li>Occasion-specific information</li>
                                    </ul>
                                </div>
                            </div>

                            <div class="card">
                                <div class="card-icon">
                                    <i class="fas fa-images"></i>
                                </div>
                                <h3 class="card-title">Image Chunk Strategy</h3>
                                <div class="card-content">
                                    <p>Multiple product images are processed as individual searchable entities:</p>
                                    <div class="code-block">// Multiple image handling
docs = [
    Document(
        page_content=image_encoding,
        metadata=self.update_metadata(
            metadata, 
            field='image', 
            _type='image'
        )
    )
    for image_encoding in product['image_encodings']
]</div>
                                    <ul class="feature-list">
                                        <li>Each image becomes separate document</li>
                                        <li>Maintains product context via metadata</li>
                                        <li>Enables fine-grained visual search</li>
                                        <li>Supports multi-angle product views</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="semantic-chunking" class="tab-content">
                        <div class="card-grid">
                            <div class="card">
                                <div class="card-icon">
                                    <i class="fas fa-brain"></i>
                                </div>
                                <h3 class="card-title">Semantic Coherence</h3>
                                <div class="card-content">
                                    <p>Chunking strategies that preserve meaning and context:</p>
                                    <ul class="feature-list">
                                        <li><strong>Sentence-based splitting:</strong> Maintains grammatical units</li>
                                        <li><strong>Topic coherence:</strong> Groups related concepts together</li>
                                        <li><strong>Contextual boundaries:</strong> Respects natural information breaks</li>
                                        <li><strong>Overlap strategies:</strong> Preserves context across chunks</li>
                                    </ul>
                                    <div class="highlight">
                                        <strong>Example:</strong> Color information includes both the color name and its descriptions 
                                        as a single semantic unit, ensuring retrieval quality.
                                    </div>
                                </div>
                            </div>

                            <div class="card">
                                <div class="card-icon">
                                    <i class="fas fa-ruler"></i>
                                </div>
                                <h3 class="card-title">Size Optimization</h3>
                                <div class="card-content">
                                    <p>Balancing chunk size for optimal retrieval performance:</p>
                                    <div class="metrics-grid">
                                        <div class="metric-card">
                                            <span class="metric-value">77</span>
                                            <span class="metric-label">Max Text Tokens</span>
                                        </div>
                                        <div class="metric-card">
                                            <span class="metric-value">512</span>
                                            <span class="metric-label">CLIP Embedding Dim</span>
                                        </div>
                                        <div class="metric-card">
                                            <span class="metric-value">10</span>
                                            <span class="metric-label">Retrieved Results</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="optimization" class="tab-content">
                        <div class="card">
                            <div class="card-icon">
                                <i class="fas fa-cogs"></i>
                            </div>
                            <h3 class="card-title">Performance Optimizations</h3>
                            <div class="card-content">
                                <h4>Metadata-Driven Efficiency</h4>
                                <ul class="feature-list">
                                    <li>Type-specific processing paths (_type metadata)</li>
                                    <li>Field-based filtering for targeted search</li>
                                    <li>Hierarchical document relationships</li>
                                    <li>Batch processing for similar content types</li>
                                </ul>

                                <h4>Memory and Storage</h4>
                                <ul class="feature-list">
                                    <li>Base64 encoding reduces storage overhead</li>
                                    <li>Lazy loading of parent documents</li>
                                    <li>Efficient vector indexing in ChromaDB</li>
                                    <li>GPU memory optimization for embeddings</li>
                                </ul>

                                <h4>Quality Assurance</h4>
                                <ul class="feature-list">
                                    <li>Consistent metadata schemas</li>
                                    <li>Validation of chunk completeness</li>
                                    <li>Embedding quality monitoring</li>
                                    <li>Search relevance feedback loops</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- RAG Evaluation Section -->
            <section id="evaluation" class="section">
                <div class="section-header">
                    <h2 class="section-title">RAG Evaluation Methods</h2>
                    <p class="section-description">
                        Comprehensive evaluation framework covering retrieval quality, generation accuracy, 
                        and multimodal performance metrics for continuous system improvement.
                    </p>
                </div>

                <div class="card-grid">
                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-bullseye"></i>
                        </div>
                        <h3 class="card-title">Retrieval Metrics</h3>
                        <div class="card-content">
                            <h4>Core Retrieval Evaluation</h4>
                            <ul class="feature-list">
                                <li><strong>Precision@K:</strong> Accuracy of top-K retrieved documents</li>
                                <li><strong>Recall@K:</strong> Coverage of relevant documents in top-K</li>
                                <li><strong>MAP (Mean Average Precision):</strong> Overall ranking quality</li>
                                <li><strong>NDCG:</strong> Normalized discounted cumulative gain</li>
                            </ul>
                            
                            <div class="code-block">// Evaluation pipeline
def evaluate_retrieval(queries, ground_truth):
    results = {}
    for k in [1, 5, 10]:
        precision_scores = []
        recall_scores = []
        
        for query, relevant_docs in zip(queries, ground_truth):
            retrieved = retriever.get_relevant_documents(query)[:k]
            retrieved_ids = [doc.metadata['id'] for doc in retrieved]
            
            precision = len(set(retrieved_ids) & set(relevant_docs)) / k
            recall = len(set(retrieved_ids) & set(relevant_docs)) / len(relevant_docs)
            
            precision_scores.append(precision)
            recall_scores.append(recall)
        
        results[f'precision@{k}'] = np.mean(precision_scores)
        results[f'recall@{k}'] = np.mean(recall_scores)
    
    return results</div>

                            <div class="metrics-grid">
                                <div class="metric-card">
                                    <span class="metric-value">0.87</span>
                                    <span class="metric-label">Precision@10</span>
                                </div>
                                <div class="metric-card">
                                    <span class="metric-value">0.72</span>
                                    <span class="metric-label">Recall@10</span>
                                </div>
                                <div class="metric-card">
                                    <span class="metric-value">0.79</span>
                                    <span class="metric-label">F1-Score</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-eye"></i>
                        </div>
                        <h3 class="card-title">Multimodal Evaluation</h3>
                        <div class="card-content">
                            <h4>Cross-Modal Assessment</h4>
                            <ul class="feature-list">
                                <li><strong>Image-to-Text Retrieval:</strong> Visual query → text results accuracy</li>
                                <li><strong>Text-to-Image Retrieval:</strong> Text query → image results quality</li>
                                <li><strong>Semantic Alignment:</strong> CLIP embedding space coherence</li>
                                <li><strong>Modal Balance:</strong> Performance parity across modalities</li>
                            </ul>

                            <div class="highlight">
                                <h4>Evaluation Challenges</h4>
                                <p><strong>Subjective Relevance:</strong> Fashion and style preferences vary significantly across users</p>
                                <p><strong>Multi-faceted Matching:</strong> Products match queries on color, style, occasion, or season</p>
                                <p><strong>Visual Similarity:</strong> Perceptual similarity vs. semantic similarity trade-offs</p>
                            </div>

                            <div class="code-block">// Cross-modal evaluation
def evaluate_cross_modal(text_queries, image_queries, 
                        text_corpus, image_corpus):
    
    # Text query → Image results
    t2i_scores = []
    for query in text_queries:
        results = retriever.similarity_search(query, k=10)
        image_results = [r for r in results if r.metadata['_type'] == 'image']
        t2i_scores.append(evaluate_relevance(query, image_results))
    
    # Image query → Text results  
    i2t_scores = []
    for img_query in image_queries:
        results = retriever.similarity_search_by_vector(
            clip_model.embed_image(img_query), k=10
        )
        text_results = [r for r in results if r.metadata['_type'] != 'image']
        i2t_scores.append(evaluate_relevance(img_query, text_results))
    
    return {
        'text_to_image_accuracy': np.mean(t2i_scores),
        'image_to_text_accuracy': np.mean(i2t_scores)
    }</div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h3 class="card-title">Generation Quality</h3>
                        <div class="card-content">
                            <h4>End-to-End RAG Evaluation</h4>
                            <ul class="feature-list">
                                <li><strong>Faithfulness:</strong> Generated content aligns with retrieved docs</li>
                                <li><strong>Answer Relevancy:</strong> Response directly addresses the query</li>
                                <li><strong>Context Utilization:</strong> Effective use of retrieved information</li>
                                <li><strong>Hallucination Detection:</strong> Identifying generated vs. retrieved facts</li>
                            </ul>

                            <div class="code-block">// Generation evaluation framework
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy, 
    context_precision,
    context_recall
)

# Evaluation dataset
eval_dataset = Dataset.from_dict({
    "question": test_questions,
    "answer": generated_answers, 
    "contexts": retrieved_contexts,
    "ground_truths": reference_answers
})

# Comprehensive evaluation
result = evaluate(
    eval_dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
)

print(f"Faithfulness: {result['faithfulness']:.3f}")
print(f"Answer Relevancy: {result['answer_relevancy']:.3f}")
print(f"Context Precision: {result['context_precision']:.3f}")
print(f"Context Recall: {result['context_recall']:.3f}")</div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <h3 class="card-title">Human Evaluation</h3>
                        <div class="card-content">
                            <h4>User-Centric Assessment</h4>
                            <ul class="feature-list">
                                <li><strong>Relevance Scoring:</strong> Human judges rate result quality</li>
                                <li><strong>A/B Testing:</strong> Compare different retrieval strategies</li>
                                <li><strong>Task Success Rate:</strong> Users complete intended actions</li>
                                <li><strong>Satisfaction Metrics:</strong> User experience and preference</li>
                            </ul>

                            <div class="metrics-grid">
                                <div class="metric-card">
                                    <span class="metric-value">4.2/5</span>
                                    <span class="metric-label">User Satisfaction</span>
                                </div>
                                <div class="metric-card">
                                    <span class="metric-value">89%</span>
                                    <span class="metric-label">Task Completion</span>
                                </div>
                                <div class="metric-card">
                                    <span class="metric-value">2.3s</span>
                                    <span class="metric-label">Avg Response Time</span>
                                </div>
                            </div>

                            <div class="highlight">
                                <h4>Evaluation Best Practices</h4>
                                <p><strong>Diverse Test Sets:</strong> Include various query types, modalities, and difficulty levels</p>
                                <p><strong>Regular Monitoring:</strong> Continuous evaluation with production data</p>
                                <p><strong>Bias Detection:</strong> Check for demographic or domain-specific biases</p>
                                <p><strong>Performance Degradation:</strong> Monitor for model drift over time</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Agentic Architecture Section -->
            <section id="agentic" class="section">
                <div class="section-header">
                    <h2 class="section-title">Agentic Architecture</h2>
                    <p class="section-description">
                        Intelligent agent-based workflows that orchestrate complex retrieval tasks, 
                        dynamic planning, and adaptive response generation for enhanced user experiences.
                    </p>
                </div>

                <div class="card-grid">
                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <h3 class="card-title">Agent-Based RAG Pipeline</h3>
                        <div class="card-content">
                            <h4>Multi-Agent Orchestration</h4>
                            <div class="architecture-diagram">
                                <div class="flow-step">Query Router Agent</div>
                                <span class="arrow">↓</span>
                                <div class="flow-step">Retrieval Planner</div>
                                <span class="arrow">↓</span>
                                <div class="flow-step">Multi-Modal Retriever</div>
                                <span class="arrow">↓</span>
                                <div class="flow-step">Context Synthesizer</div>
                                <span class="arrow">↓</span>
                                <div class="flow-step">Response Generator</div>
                            </div>

                            <div class="code-block">// Agent coordination example
class RAGOrchestrator:
    def __init__(self):
        self.query_router = QueryRouterAgent()
        self.planner = RetrievalPlannerAgent() 
        self.retriever = MultiModalRetrieverAgent()
        self.synthesizer = ContextSynthesizerAgent()
        self.generator = ResponseGeneratorAgent()
    
    async def process_query(self, query):
        # Route and classify query
        query_type = await self.query_router.classify(query)
        
        # Plan retrieval strategy
        plan = await self.planner.create_plan(query, query_type)
        
        # Execute retrieval
        contexts = await self.retriever.execute_plan(plan)
        
        # Synthesize and rank contexts
        synthesized = await self.synthesizer.process(contexts, query)
        
        # Generate final response
        response = await self.generator.generate(query, synthesized)
        
        return response</div>

                            <ul class="feature-list">
                                <li>Specialized agents for different pipeline stages</li>
                                <li>Dynamic strategy adaptation based on query type</li>
                                <li>Parallel processing for improved performance</li>
                                <li>Fault tolerance and graceful degradation</li>
                            </ul>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-brain"></i>
                        </div>
                        <h3 class="card-title">Adaptive Query Planning</h3>
                        <div class="card-content">
                            <h4>Intelligent Retrieval Strategies</h4>
                            <ul class="feature-list">
                                <li><strong>Query Analysis:</strong> Intent detection and complexity assessment</li>
                                <li><strong>Strategy Selection:</strong> Choose optimal retrieval approach</li>
                                <li><strong>Dynamic Refinement:</strong> Iterative query expansion and filtering</li>
                                <li><strong>Multi-step Reasoning:</strong> Break complex queries into sub-tasks</li>
                            </ul>

                            <div class="code-block">// Adaptive planning agent
class RetrievalPlannerAgent:
    def analyze_query(self, query):
        return {
            'complexity': self.assess_complexity(query),
            'modality': self.detect_modality_preference(query),
            'intent': self.classify_intent(query),
            'specificity': self.measure_specificity(query)
        }
    
    def create_plan(self, query, analysis):
        if analysis['complexity'] == 'simple':
            return SingleStepPlan(query, k=10)
        
        elif analysis['complexity'] == 'multi_faceted':
            return MultiStepPlan([
                ('color', self.extract_color_terms(query)),
                ('style', self.extract_style_terms(query)), 
                ('occasion', self.extract_occasion_terms(query))
            ])
        
        elif analysis['complexity'] == 'comparative':
            return ComparativePlan(
                base_query=query,
                comparison_dimensions=self.extract_comparisons(query)
            )</div>

                            <div class="highlight">
                                <h4>Planning Strategies</h4>
                                <p><strong>Simple Queries:</strong> Direct semantic search with standard k=10 retrieval</p>
                                <p><strong>Complex Queries:</strong> Decompose into sub-queries, retrieve separately, then synthesize</p>
                                <p><strong>Comparative Queries:</strong> Retrieve candidates, perform side-by-side analysis</p>
                                <p><strong>Exploratory Queries:</strong> Iterative refinement with user feedback loops</p>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-sync-alt"></i>
                        </div>
                        <h3 class="card-title">Self-Improving Systems</h3>
                        <div class="card-content">
                            <h4>Continuous Learning Architecture</h4>
                            <ul class="feature-list">
                                <li><strong>Performance Monitoring:</strong> Real-time quality assessment</li>
                                <li><strong>Feedback Integration:</strong> User interactions inform improvements</li>
                                <li><strong>Strategy Evolution:</strong> Adapt retrieval patterns over time</li>
                                <li><strong>Knowledge Updates:</strong> Incorporate new product data dynamically</li>
                            </ul>

                            <div class="code-block">// Self-improvement feedback loop
class AdaptiveRAGSystem:
    def __init__(self):
        self.performance_tracker = PerformanceTracker()
        self.strategy_optimizer = StrategyOptimizer()
        self.feedback_processor = FeedbackProcessor()
    
    def process_with_learning(self, query):
        # Execute query with current strategy
        result = self.execute_query(query)
        
        # Collect performance metrics
        metrics = self.performance_tracker.measure(query, result)
        
        # Process user feedback if available
        if self.has_feedback(query):
            feedback = self.feedback_processor.extract(query)
            self.strategy_optimizer.update_strategy(query, metrics, feedback)
        
        # Adapt future behavior
        self.update_retrieval_weights(metrics)
        
        return result
    
    def update_retrieval_weights(self, metrics):
        if metrics['precision'] < 0.7:
            self.increase_semantic_threshold()
        if metrics['diversity'] < 0.5:
            self.enable_diversification()
        if metrics['response_time'] > 3.0:
            self.optimize_retrieval_count()</div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-icon">
                            <i class="fas fa-network-wired"></i>
                        </div>
                        <h3 class="card-title">Multi-Agent Collaboration</h3>
                        <div class="card-content">
                            <h4>Specialized Agent Ecosystem</h4>

                            <div class="tab-container">
                                <div class="tab-buttons">
                                    <button class="tab-button active" onclick="switchTab(event, 'agent-types')">Agent Types</button>
                                    <button class="tab-button" onclick="switchTab(event, 'communication')">Communication</button>
                                    <button class="tab-button" onclick="switchTab(event, 'coordination')">Coordination</button>
                                </div>

                                <div id="agent-types" class="tab-content active">
                                    <ul class="feature-list">
                                        <li><strong>Query Router:</strong> Classifies intent and routes to appropriate agents</li>
                                        <li><strong>Context Gatherer:</strong> Specialized retrieval from different modalities</li>
                                        <li><strong>Relevance Ranker:</strong> Scores and orders retrieved content</li>
                                        <li><strong>Response Composer:</strong> Synthesizes final user-facing response</li>
                                        <li><strong>Quality Assessor:</strong> Evaluates output quality and triggers refinement</li>
                                        <li><strong>Learning Agent:</strong> Captures insights for system improvement</li>
                                    </ul>
                                </div>

                                <div id="communication" class="tab-content">
                                    <div class="code-block">// Inter-agent communication
class AgentCommunicationProtocol:
    def __init__(self):
        self.message_bus = MessageBus()
        self.agent_registry = AgentRegistry()
    
    def broadcast_query_update(self, query_id, update):
        interested_agents = self.agent_registry.get_subscribers(
            topic=f"query.{query_id}"
        )
        
        for agent in interested_agents:
            self.message_bus.send(agent, {
                'type': 'query_update',
                'query_id': query_id,
                'data': update,
                'timestamp': datetime.now()
            })
    
    def request_collaboration(self, requesting_agent, task):
        capable_agents = self.agent_registry.find_capable(
            task.required_capabilities
        )
        
        responses = []
        for agent in capable_agents:
            response = self.message_bus.request(agent, {
                'type': 'collaboration_request',
                'task': task,
                'deadline': task.deadline
            })
            responses.append(response)
        
        return self.select_best_collaborator(responses)</div>
                                </div>

                                <div id="coordination" class="tab-content">
                                    <ul class="feature-list">
                                        <li><strong>Task Distribution:</strong> Parallel processing across specialized agents</li>
                                        <li><strong>Resource Management:</strong> Load balancing and capacity planning</li>
                                        <li><strong>Conflict Resolution:</strong> Handle disagreements between agents</li>
                                        <li><strong>Consensus Building:</strong> Aggregate opinions for final decisions</li>
                                        <li><strong>Failure Handling:</strong> Graceful degradation when agents fail</li>
                                    </ul>

                                    <div class="highlight">
                                        <h4>Benefits of Agentic Architecture</h4>
                                        <p><strong>Modularity:</strong> Easy to add, remove, or modify individual agents</p>
                                        <p><strong>Scalability:</strong> Distribute workload across multiple processing units</p>
                                        <p><strong>Specialization:</strong> Each agent optimized for specific tasks</p>
                                        <p><strong>Robustness:</strong> System continues functioning even if some agents fail</p>
                                        <p><strong>Adaptability:</strong> Dynamic reconfiguration based on changing requirements</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 Multimodal RAG System - Advanced AI Architecture Documentation</p>
            <p>Built with modern web technologies and comprehensive technical analysis</p>
        </div>
    </footer>

    <script>
        // Scroll indicator
        window.addEventListener('scroll', () => {
            const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            document.querySelector('.scroll-indicator').style.width = scrollPercent + '%';
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Tab switching functionality
        function switchTab(evt, tabName) {
            const tabContents = document.querySelectorAll('.tab-content');
            const tabButtons = document.querySelectorAll('.tab-button');
            
            tabContents.forEach(content => content.classList.remove('active'));
            tabButtons.forEach(button => button.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
        }

        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe all cards for animation
        document.querySelectorAll('.card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    </script>
</body>
</html>
