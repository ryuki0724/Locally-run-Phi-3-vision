# Locally run Phi3-Vision on Windows with gpu
Locally deploy Phi-3-Vision - Text, Single Image, Multiple Images, N Images
## Step 1: Download the Phi-3 Vision Model
1. Navigate to the [Hugging Face page for Phi-3 Vision](https://huggingface.co/microsoft/Phi-3-vision-128k-instruct).
2. Click on the "Files and versions" tab.
3. Download the necessary model files to your local machine.
## Step 2: Install Required Dependencies
1. Visit the [Phi-3 Cookbook repository](https://github.com/microsoft/Phi-3CookBook).
2. Follow the provided instructions to set up your environment and install all required dependencies.

## Copyright and License
This project uses the Phi-3 Vision model created by Microsoft. Please refer to the [original license](https://huggingface.co/microsoft/Phi-3-vision-128k-instruct/blob/main/LICENSE) for usage terms. We are grateful to Microsoft for making this model publicly available.

## Run the Phi-3 Vision Model
1. Ensure that the model files are correctly placed as per the instructions.
2. Use the following command to run the model:
   ```bash
   python phi3_vision.py
   ```

## Example
In the terminal, type in your input as follows:
### For Text Input:
   ```bash
   what is the number of 2+2?
   ```
### For Single Image Input:
   ```bash
   Could you please introduce this stock to me? --path "path-to-your-stock-image"
   ```
### For Multiple Images Input:
   ```bash
   What is difference in this two images? --path "path-to-your-image1" "path-to-your-image2"
   ```
### Troubleshooting
If you encounter any issues, please check the following:
1. Ensure all dependencies are correctly installed.
2. Verify that your GPU drivers are up to date.
3. Check that the model files are placed in the correct directory.

For more detailed troubleshooting, please refer to the [Phi-3 Cookbook](https://github.com/microsoft/Phi-3CookBook) or open an issue in this repository.

## Contributing
We welcome contributions!

## Changelog
- v1.0: Initial release

## Contact
For any questions or issues, please open an issue in this repository.

## Performance Note
Please be aware that running this model may require significant computational resources and time, especially for complex inputs or multiple images.
