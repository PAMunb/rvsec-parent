import logging
import os
from typing import List, Dict, Any

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# Configure logging (do this once at the module level)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)  # Use a more specific logger name


class HuggingFaceLLM:  # More descriptive class name
    """
    A class for interacting with Hugging Face language models.

    Attributes:
        model_name (str): The name of the pre-trained model to use.
        _model (AutoModelForCausalLM): The loaded language model (lazy-loaded).
        _tokenizer (AutoTokenizer): The tokenizer for the model (lazy-loaded).
        _device (str): The device to use for model inference (e.g., "cuda", "cpu").
    """

    def __init__(self, model_name: str, device: str = "cuda"):
        """Initializes the HuggingFaceLLM with a model name and device."""
        self.model_name = model_name
        self._model = None
        self._tokenizer = None
        self._device = device  # Store the device

    @property
    def model(self) -> AutoModelForCausalLM:
        """Loads and returns the language model (lazy-loaded)."""
        if self._model is None:
            logger.info(f"Loading model {self.model_name} on {self._device}...")
            try:
                quantization_config = BitsAndBytesConfig(  # More descriptive variable name
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,  # Consider float16 if bfloat16 is not supported
                    bnb_4bit_quant_type="nf4",
                )

                self._model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    device_map=self._device,  # Use the stored device
                    quantization_config=quantization_config,
                    torch_dtype=torch.bfloat16 # Consider float16 if bfloat16 is not supported
                )
                # if torch.cuda.is_available():
                #     print("GPU está disponível")
                #     # device = torch.device("cuda")  # Define o dispositivo como GPU
                # else:
                #     print("GPU não está disponível")
                #     # device = torch.device("cpu") 
                if self._device == "cuda": # Only move to cuda if available
                    self._model.to(self._device) # Explicit move to device after loading
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise  # Re-raise the exception for proper handling
        return self._model

    @property
    def tokenizer(self) -> AutoTokenizer:
        """Loads and returns the tokenizer (lazy-loaded)."""
        if self._tokenizer is None:
            logger.info(f"Loading tokenizer for {self.model_name}...")
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            tokenizer.pad_token = tokenizer.eos_token  # Set pad token if needed
            self._tokenizer = tokenizer
        return self._tokenizer

    def generate(self, messages: List[Dict[str, str]], max_new_tokens: int = 800) -> str:
        """Generates text based on the given messages."""

        inputs = self.tokenizer.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True
        ).to(self._device)  # Use the correct device

        with torch.no_grad():  # Important for inference
            outputs = self.model.generate(inputs, max_new_tokens=max_new_tokens)

        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        del inputs, outputs # Explicitly delete tensors to free memory
        torch.cuda.empty_cache() # Explicitly clear CUDA cache after generation
        return result

    def clean(self):
        """Unloads the model and tokenizer from memory."""

        if hasattr(self, '_model') and self._model is not None:
            del self._model
            self._model = None

        if hasattr(self, '_tokenizer') and self._tokenizer is not None:
            del self._tokenizer
            self._tokenizer = None

        torch.cuda.empty_cache()  # Clear CUDA cache
        logger.info("Model and tokenizer unloaded, CUDA cache cleared.")