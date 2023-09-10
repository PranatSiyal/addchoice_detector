import imghash from "imghash";
import leven from "leven";
import { promises as fs } from "fs"; // Import fs module with promises
import path from "path";

async function compareImages() {
  try {
    const hash1 = await imghash.hash("output2_image.png");
    //const hash2 = await imghash.hash("CNN/A-photo-of-a-person-tapping-on-a-smartphone-in-front-of-a-MacBook-with-dollar-signs-coming-out-from-the-phone.jpg");
    const imageFiles = await fs.readdir("/Users/pranatsiyal/addchoice_detector/output_newyorker");
    var count_P = 0
    var count_N = 0
    for (const imageFile of imageFiles) {
        const image2Path = path.join("/Users/pranatsiyal/addchoice_detector/output_newyorker", imageFile);
        //const extractedImage = await extractTopRight(image2Path);
        //const extractedImageHash = await imghash.hashBuffer(extractedImageBuffer);

        //const extractedImageBuffer = Buffer.from(extractedImage.data);

        // Convert the buffer to a string for Levenshtein comparison
        //const extractedImageHash = extractedImageBuffer.toString();

        const hash2 = await imghash.hash(image2Path);
        const distance = leven(hash1, hash2);
        // console.log(`Distance between images is: ${distance}`);
        
        // const hash2 = await imghash.hash(image2Path);
        // const distance = leven(hash1, hash2);
        // console.log(`Distance between images is: ${distance}`);

        if (distance <= 13) {
          console.log("Images are similar distance: ${distance}", imageFile);
          count_P++
          console.log(count_P)
        } else {
          // console.log("Images are NOT similar", imageFile);
          count_N++
          console.log(count_N)
        }
        }
  } catch (error) {
    console.error("Error:", error);
  }
}
compareImages();