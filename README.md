<h1 align="center">Governor's Cup Championship in Computer Vision and Artificial Intelligence of the Novosibirsk Region</h1>

<h2 align="center">Tasks</h2>

<h3 align="center">Product quality control</h3>

<h4 align="justify">The video shows the movement of the nuts along the conveyor. The nuts are moved from the bottom of the frame to the top. Among the nuts there are defective ones, they are deformed and have distorted contours. For each nut captured on video, it is necessary to determine compliance with quality standards. Each nut must be assigned a number: 1 for defective nuts, 0 for quality ones. For each video file, you should get a list of 0 and 1. The first digit in the list corresponds to the first nut that appeared in the frame.</h4>

<div style="text-align: center;"><img src="https://github.com/EgorAndrik/avt-Computer-Vision-Championship/blob/main/ForREADME/263394779-929e99b8-ec18-4d43-8519-d873d24eaaf1.png"></div>

The 96% accuracy solution is presented in [folder](Product_quality_control).

<h3 align="center">Known logo detection</h3>

<h4 align="justify">The image shows the logo. Your task is to write a function that determines in which part of the image the logo is located, and what it is called. Each image features one of the five logos. Possible logos:</h4>
<div style="text-align: center;"><img src="https://github.com/EgorAndrik/avt-Computer-Vision-Championship/blob/main/ForREADME/logos.png"></div>

<h4 align="justify">Your function should return the name of the logo and the coordinates of the logo's bounding box. Correctly detected and recognized are those logos for which the name is correctly specified and IoU is greater than 0.5.</h4>
<div style="text-align: center;"><img src="https://github.com/EgorAndrik/avt-Computer-Vision-Championship/blob/main/ForREADME/263394831-b9b194c3-671a-4301-ba72-4e4275cd3076.png"></div>

The 100% accuracy solution is presented in [folder](Logo_detection).

<h3 align="center">Classification of road signs</h3>

<h4 align="justify">The images show traffic signs. Each image has exactly one character. Your task is to write a function that determines which of the eight characters in the image. Possible signs:</h4>
<div style="text-align: center;"><img src="https://github.com/EgorAndrik/avt-Computer-Vision-Championship/blob/main/ForREADME/263394894-1b3e597d-35ff-4104-9acb-b0c2f2c2bdae.png"></div>

The 100% accuracy solution is presented in [folder](Classification_of_road_signs).

<h3 align="center">Traffic light detection</h3>

<h4 align="justify">The images show traffic lights. Your task is to write a function that determines in which part of the image the traffic light is located. There is only one traffic light in each image. The function must return the coordinates of the traffic light's bounding box. Traffic lights for which IoU is greater than 0.5 are considered to be correctly detected.</h4>

<div style="text-align: center;"><img src="https://github.com/EgorAndrik/avt-Computer-Vision-Championship/blob/main/ForREADME/263394831-b9b194c3-671a-4301-ba72-4e4275cd3076.png"></div>

The 100% accuracy solution is presented in [folder](Traffic_light_detection).
