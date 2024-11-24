# wildfire


### Compiling from Source

Start by cloning the repository using the `--recursive` flag, as there are submodules that need to be downloaded along with the main code.

We use CMake as the build system, so please install it along with a compiler or an IDE (for Windows).

- **Website:**

  Just run this script:
npm run dev in the wildfire project

to run backend run the python main.py in the api folder 

to run model locan on the drone run the python main.py in the model forder 

├── api
│   ├── getimg.py
│   ├── main.py
│   ├── satellite_image.jpg
│   └── test.py
├── model
│   ├── data.yaml
|   ├── main.py
│   ├── README.dataset.txt
│   ├── README.roboflow.txt
│   ├── runs
│   ├── test
│   ├── test.txt
│   ├── train
│   ├── valid
│   ├── yolo11n.pt
│   └── yolov8n.pt
├── README.md
└── wildfire
    ├── eslint.config.js
    ├── index.html
    ├── node_modules
    ├── package.json
    ├── package-lock.json
    ├── public
    ├── README.md
    ├── src
    └── vite.config.js

11 directories, 17 files
