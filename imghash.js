import imghash from "imghash";
import leven from "leven";
import { promises as fs } from "fs"; // Import fs module with promises
import path from "path";
async function compareImages() {
  try {
    const hash1 = await imghash.hash("choices-or-truste-tr.png");
    //const hash2 = await imghash.hash("CNN/A-photo-of-a-person-tapping-on-a-smartphone-in-front-of-a-MacBook-with-dollar-signs-coming-out-from-the-phone.jpg");
    const imageFiles = await fs.readdir("/Users/pranatsiyal/addchoice_detector/rando_screenshots");

    for (const imageFile of imageFiles) {
      const image2Path = path.join("/Users/pranatsiyal/addchoice_detector/rando_screenshots", imageFile);

      const hash2 = await imghash.hash(image2Path);
      const distance = leven(hash1, hash2);
      console.log(`Distance between images is: ${distance}`);

      if (distance <= 12) {
        console.log("Images are similar", imageFile);
      } else {
        console.log("Images are NOT similar");
      }
      }
  } catch (error) {
    console.error("Error:", error);
  }
}


compareImages();
