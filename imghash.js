
import imghash from "imghash";
import leven from "leven";
async function compareImages() {
  try {
    const hash1 = await imghash.hash("oba_small.png");
    const hash2 = await imghash.hash("random.png");

    const distance = leven(hash1, hash2);
    console.log(`Distance between images is: ${distance}`);

    if (distance <= 12) {
      console.log("Images are similar");
    } else {
      console.log("Images are NOT similar");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

compareImages();
