
# NewCoPho | New Context Photos

Replace anything that's not a 'person' in your photo with a new Background Image.
Uses PyTorch, Deeplabv3, ResNet101
Requires CUDA!

## Examples
|<img src="https://user-images.githubusercontent.com/737888/72228119-d418a300-3558-11ea-9757-88774d7ac820.jpg" width="180" height="320" />  | <img src="https://user-images.githubusercontent.com/737888/72228127-e0046500-3558-11ea-8b8a-884d65bb08d8.jpg" width = "180" height = "320" /> |
|--|--|
|<img src="https://user-images.githubusercontent.com/737888/72228120-d418a300-3558-11ea-957e-311c7977661e.jpg" width="320" height="180" />  | <img src="https://user-images.githubusercontent.com/737888/72228128-e0046500-3558-11ea-931c-4382c4b8b1c8.jpg" width = "320" height = "180" /> |

## Windows Quickstart
1. Install [Python 3.6](https://www.python.org/downloads/)
2. Create Virtual Environment
 `python -m venv env`
3. Activate the Environment
 `"env/Scripts/activate"`
4. Install Requirements
`pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html`
5. Run the Server    
`flask run --host 0.0.0.0`
6. Visit on Mobile Device
    http://your.ip.address:5000 
    

## Quickstart Breakdown

#### Create Virtual Environment

This keeps all the dependencies for this project separate from other Python projects you may work on.

On Windows, run:

`python -m venv env`, which will create a virtual environment in a folder named 'env'.

You then 'activate' this environment by running this in a command prompt: `"env/Scripts/activate"`, which runs the activate.bat script. You need the double quotes for Windows to understand the command. Once you run this, your prompt should update to show `(env)` instead of `C:\FolderName` or wherever you saved the project.

#### Install Requirements.

The requirements have been saved into the requirements.txt file, so you can install this file with this command:

`pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html`

The -f argument points pip towards the right place to download the torch and torchvision dependencies. This command fails for me without this argument.

If you have issues with PyTorch, you can install it for a specific Python + Cuda version using the instructions [here](https://pytorch.org/get-started/locally/).


## Execution  

#### Run the Server.

I do it this way: `flask run --host 0.0.0.0`, which will start the server in a way that other machines on your local network can access the host.


#### Visit the page in a browser (mobile browsers best).
Get your ip and visit it in a browser on port 5000. It will be something like http://192.168.1.15:5000


## Customization

Change the BGPortrait.jpg and BGLandscape.jpg files in the /media folder to use your own background images.


## Credits

Loading Icon and Backgrounds from [loading.io](https://loading.io)
Image Segmentation based on [this colab notebook](https://colab.research.google.com/github/pytorch/pytorch.github.io/blob/master/assets/hub/pytorch_vision_deeplabv3_resnet101.ipynb) from the Pytorch team.
