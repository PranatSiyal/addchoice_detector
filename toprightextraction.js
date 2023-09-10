import { createCanvas, loadImage } from "canvas";
import fs from "fs";
import path from "path"; // Import the path module

async function extractTopRight(imgPath) {
  const canvas = createCanvas(30, 15);
  const ctx = canvas.getContext("2d");

  const img = await loadImage(imgPath);
  ctx.drawImage(img, img.width - 30, 0, 30, 15, 0, 0, 30, 15);

  // Get the extracted image data
  const extractedImageData = ctx.getImageData(0, 0, 30, 15);

  return extractedImageData;
}

(async () => {
  try {

    const outputDirectory = "output_newyorker";
    await fs.promises.mkdir(outputDirectory, { recursive: true });
    const imageFiles = await fs.promises.readdir("/Users/pranatsiyal/addchoice_detector/newyorker_screenshots");
    for (const imageFile of imageFiles) {
        const imagePath = path.join("/Users/pranatsiyal/addchoice_detector/newyorker_screenshots", imageFile);
  
        const extractedImage = await extractTopRight(imagePath);
  
        // Create a new canvas to draw the extracted image data
        const newCanvas = createCanvas(30, 15);
        const newCtx = newCanvas.getContext("2d");
        newCtx.putImageData(extractedImage, 0, 0);
  
        // Save the new canvas as an image file
        const outputImagePath = path.join(outputDirectory, `output_${imageFile}`);
        const stream = fs.createWriteStream(outputImagePath);
        const buffer = newCanvas.toBuffer("image/png");
        stream.write(buffer);
        stream.end();
        console.log(`Extracted image saved as ${outputImagePath}`);
    
    // const extractedImage = await extractTopRight("/Users/pranatsiyal/addchoice_detector/test_screenshots/img_1.png");
    

    // // Create a new canvas to draw the extracted image data
    // const newCanvas = createCanvas(30, 15);
    // const newCtx = newCanvas.getContext("2d");
    // newCtx.putImageData(extractedImage, 0, 0);

    // // Save the new canvas as an image file
    // const outputImagePath = "output2_image.png";
    // const stream = fs.createWriteStream(outputImagePath);
    // const buffer = newCanvas.toBuffer("image/png");
    // stream.write(buffer);
    // stream.end();
    // console.log(`Extracted image saved as ${outputImagePath}`);
    }
  } catch (error) {
    console.error("Error:", error);
  }
})();