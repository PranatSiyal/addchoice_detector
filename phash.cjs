const fs = require('fs').promises;
const path = require('path');
const { createCanvas, loadImage } = require('canvas');

async function pHash(imgPath) {
    const size = 32,
        smallerSize = 8;

    const canvas = createCanvas(size, size),
        ctx = canvas.getContext('2d');

    const img = await loadImage(imgPath);

    //top right crop
    const cropWidth = 30;
    const cropHeight = 19;
    const cropCanvas = createCanvas(cropWidth, cropHeight);
    const cropCtx = cropCanvas.getContext('2d');
    
    //till here top right crop

    ctx.drawImage(img, 0, 0, size, size);
    const im = ctx.getImageData(0, 0, size, size);

    const vals = new Float64Array(size * size);
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const base = 4 * (size * i + j);
            vals[size * i + j] = 0.299 * im.data[base] +
                0.587 * im.data[base + 1] +
                0.114 * im.data[base + 2];
        }
    }

    function applyDCT2(N, f) {
        // Initialize coefficients
        const c = new Float64Array(N);
        for (let i = 1; i < N; i++) c[i] = 1;
        c[0] = 1 / Math.sqrt(2);
    
        // Output goes here
        const F = new Float64Array(N * N);
    
        // Construct a lookup table, because it's O(n^4)
        const entries = (2 * N) * (N - 1);
        const COS = new Float64Array(entries);
        for (let i = 0; i < entries; i++) {
            COS[i] = Math.cos((i / (2 * N)) * Math.PI);
        }
    
        // The core loop inside a loop inside a loop...
        for (let u = 0; u < N; u++) {
            for (let v = 0; v < N; v++) {
                let sum = 0;
                for (let i = 0; i < N; i++) {
                    for (let j = 0; j < N; j++) {
                        sum += COS[(2 * i + 1) * u] * COS[(2 * j + 1) * v] * f[N * i + j];
                    }
                }
                sum *= ((c[u] * c[v]) / 4);
                F[N * u + v] = sum;
            }
        }
        return F;
    }

    const dctVals = applyDCT2(size, vals);

    const median = vals.slice(0).sort((a, b) => a - b)[Math.floor(vals.length / 2)];

    const binaryHash = vals.map(e => (e > median ? '1' : '0')).join('');

    return binaryHash;
}

function distance(a, b) {
    let dist = 0;
    for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) {
            dist++;
        }
    }
    return dist;
}

async function compareImages() {
    try {
        const hash1 = await pHash('output2_image.png',12 * 13);
        const imageFiles = await fs.readdir('/Users/pranatsiyal/addchoice_detector/test_screenshots');

        for (const imageFile of imageFiles) {
            const image2Path = path.join('/Users/pranatsiyal/addchoice_detector/test_screenshots', imageFile);

            const hash2 = await pHash(image2Path, 12*13);
            const dist = distance(hash1, hash2);
            console.log(`Distance between images is: ${dist}`);

            if (dist <= 12) {
                console.log('Images are similar', imageFile);
            } else {
                console.log('Images are NOT similar');
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

compareImages();