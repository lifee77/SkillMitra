Background and Justification
The SkillMitra project is designed to harness generative AI for enhancing vocational training in developing economies. Building on the initial FaST analysis, this initiative explores the integration of audio and image generation models to produce engaging educational video content. Vocational training remains a critical need in many regions, where traditional educational resources are limited. By using a pipeline that iteratively prompts generative models, SkillMitra aims to create tailored learning experiences that adapt to user backgrounds and local employability challenges. The project draws inspiration from educational platforms such as Khan Academy and Duolingo, which have successfully employed digital content and gamification strategies to boost learner engagement. In addition, recent advances in ML-based content generation and fine-tuning for local languages (for instance, Nepali) provide a strong technological foundation. The emphasis on a mobile-first approach and offline capabilities ensures accessibility in areas with low bandwidth, thereby addressing both technical and socioeconomic challenges. This background supports the project’s relevance and potential for impactful innovation in educational delivery.

3. Project Description
SkillMitra is a generative AI project aimed at producing coherent educational videos for vocational training. The project leverages a pipeline that combines audio and image generation models to create content ranging from one to five minutes. The methodology involves several phases: data cleaning and preprocessing of curriculum-related metadata, development and fine-tuning of generative ML models, and integration of these models into a robust ML pipeline. 

Our video generation pipeline is pretty cool - it takes text input from our curriculum database and transforms it into engaging visual content through these steps:
   - Text processing: We break down lesson content into manageable chunks
   - Script generation: Using GPT models to create conversational scripts
   - Voice synthesis: Converting scripts to realistic voiceovers (we're experimenting with different accents!)
   - Visual content creation: Generating relevant images and diagrams
   - Animation integration: Adding simple animations to illustrate concepts
   - Video assembly: Combining all elements into a cohesive video
   - Quality checking: Running automated checks for audio clarity and visual consistency

The deliverables include a minimally viable product (MVP) of the web app, a preliminary mobile app version (subject to app store approvals), and comprehensive code repositories. Extensions under consideration involve language-specific fine-tuning (targeting Nepali), an adaptive course recommendation system, gamified learning features such as quizzes and flashcards, and offline functionality to support low-bandwidth environments. This systematic approach combines economic theory with modern machine learning and robust software engineering practices to create an innovative educational tool.

4. Proof of Concept
The proof of concept includes three working prototypes:
Web App: A preliminary web application is operational, demonstrating the integration of front-end and back-end services.
Machine Learning Pipeline: Initial experiments in voice classification (documented in a dedicated GitHub repository) and model fine-tuning for generative tasks validate the technical feasibility of generating multimedia educational content.
Video Generation: We've successfully created several 1-minute demo videos using our pipeline. These videos show how our system can transform a basic lesson outline on carpentry skills into visually engaging content. The quality isn't perfect yet (some of the animations are kinda janky!), but they definitely prove that our approach works. We're still figuring out how to make the voiceover sound less robotic, but overall, the videos are clear and informative.

These prototypes provide a tangible foundation for further development and showcase the integration of diverse modules—ranging from data preprocessing to ML model deployment.

5. Presentation and Analysis of Preliminary Work Products
Preliminary work has focused on establishing core functionalities across both the web application and ML modules. The initial FaST analysis provided essential feedback, which has been incorporated into refining data cleaning methods and improving code robustness. Early testing of generative models demonstrates promising outputs in audio and image generation, while the web app prototype confirms that both front-end and back-end components interact effectively. The use of separate repositories for ML experiments and app development has enabled clearer separation of concerns and facilitated focused iterations. Feedback from peers and iterative testing have led to performance optimizations and the identification of critical next steps—particularly in fine-tuning model accuracy and ensuring the app’s scalability. This integrated approach underscores the project’s potential while outlining the necessary refinements ahead.
