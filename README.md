# Human_in_the_Loop_Reasoning
Its a finetuned DeepSeekR1 Model which asks user doubts to ambigous questions, and proceeds with its further reasoning steps. Just like <think> token in reasoning models, here <ask>, <question> tokens are used to ask user doubts. This can be used in any reasoning model to improve its accuracy as it reduces the ambiguity in the task assigned to the model and also I think this might reduce the compounding error in reasoning models.

## Model Card
- Model Name: Human_in_the_Loop_Reasoning
- Base Model: DeepSeekR1
- Fine-tuning Method: LoRA
- Dataset: Self created dataset with 5000 samples
- License: MIT License
- Model Weights: [Hugging Face Link](https://huggingface.co/RohitFrancis)
- Training Code: [GitHub Repository](https://github.com/Rohit909-creator/Human_in_the_Loop_Reasoning)
- Intended Use Cases: Enhancing reasoning tasks by incorporating user feedback to resolve ambiguities.
- Limitations: May require user interaction which could slow down the reasoning process. Performance is dependent on the quality of user input.
- Ethical Considerations: Ensure user data privacy and avoid over-reliance on user input for critical decisions.
- Citation: Please cite the GitHub repository if you use this model in your work.