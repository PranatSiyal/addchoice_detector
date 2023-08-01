const { createCanvas, loadImage } = require('canvas');

async function aHash(img) {
  const width = 25;
  const height = 25;
  const hash_padding = 3; // Pad resulting hash up to proper hash length

  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext('2d');

  ctx.drawImage(img, 0, 0, width, height);

  const im = ctx.getImageData(0, 0, width, height);

  const num_channels = 4;
  const vals = new Float64Array(width * height);

  // Convert image to grayscale
  for (let i = 0; i < width; i++) {
    for (let j = 0; j < height; j++) {
      const base = num_channels * (width * j + i);
      if (im.data[base + 3] == 0) {
        vals[width * j + i] = 255;
        continue;
      }
      vals[width * j + i] = 0.2126 * im.data[base] +
                            0.7152 * im.data[base + 1] +
                            0.0722 * im.data[base + 2];
    }
  }

  // Find average pixel value
  let pixel_sum = 0;
  for (let i = 0; i < vals.length; i++) {
    pixel_sum += vals[i];
  }
  const pixel_avg = pixel_sum / vals.length;

  let hash = '';

  // Add padding to start of hash
  for (let i = 0; i < hash_padding; i++) {
    hash += 0;
  }

  for (let i = 0; i < width; i++) {
    for (let j = 0; j < height; j++) {
      const pixel = vals[width * j + i];
      hash += pixel < pixel_avg ? 1 : 0;
    }
  }

  return hash;
}

// Example usage with two images:
async function compareImages() {
  try {
    const subsetImage = await loadImage("oba_small.png");
    const fullImage = await loadImage("adv.png");

    const subsetHash = await aHash(subsetImage);
    const fullHash = await aHash(fullImage);

    // Compare the hashes of the two images to check if the subset image matches part of the full image.
    const sim_score = 1 - distance(subsetHash, fullHash) / 628.0;

    console.log("Sim score:", sim_score);

    // Adjust the threshold value (SIM_THRESHOLD) based on your requirements to determine the match.
    const SIM_THRESHOLD = 0.9;

    // If the similarity score is above the threshold, the subsetImage is a subset of the fullImage.
    if (sim_score > SIM_THRESHOLD) {
      console.log("The subset image is a subset of the full image.");
    } else {
      console.log("The subset image is not a subset of the full image.");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

compareImages();
