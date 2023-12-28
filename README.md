# Positioning-drone
This is the software for the illegal drone detection and positioning system that I created for my scientific research. 
## Original idea
The idea is to build a system capable of detecting drones through images from two cameras by using object detection problems. We need to know in advance the position coordinates and optical axis directions of the two cameras. From there, calculate the drone's position. The picture below helps visualize the idea I mentioned
![Alt text](/image1.png)
## Tasks required to build the system
1. Building a dataset about drones.

   The drone data set needs to be large enough, the goal needs to be over 10 thousand images including two main objects: drones and birds (objects flying in the sky similar to drones). The search will prioritize publicly available drone datasets. Then, the data set was supplemented by drone videos on YouTube.

2. Conduct training and evaluate the results of object detection models on the created drone data set. Select the appropriate model for the system.

   Conduct training of the object detection models on the drone data sets built-in content 1. Evaluate the results, and edit the data set and training parameters to give results. best results. Select the appropriate model from the results to use for the general system. Training and evaluation were performed on Colab's NVIDIA Tesla V100 GPU card. Criteria to be met include accuracy over 95% and detection speed over 30 FPS.

3. Develop a drone positioning method based on images.

   Proposing drone positioning methods based on detection results. Positioning error is below 5% and positioning speed is above 100 FPS.

4. Build a web application for regional managers.

   Build a web application for regional managers to remotely monitor. The screen needs to have live images from the monitoring area through the camera and the drone's location coordinates when the drone appears in the monitoring area.

5. Building an experimental positioning system.

   Combine devices into a total system, including surveillance camera components, antenna directional devices, routers, and computers. The antenna-orienting device is built to simulate the ability to orient the antenna according to the drone's position. The router is used to link other components to the web application on the supervisor's computer.

6. Check the system's performance

   Create a script to test the system's performance. Analyze results and give comments. Conclusion of the system's strengths and weaknesses.

## My system
![Alt text](/image2.png)
## My method of conducting experiments
![Alt text](/image3.png)
