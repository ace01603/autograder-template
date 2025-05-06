// Sample solution (delete from autograder)

let cat;
let catW = 512;
let catH = 410;

function preload() {
    cat = loadImage("sketch3/assets/pallas_cat.jpg");
}

function setup() {
    createCanvas(catW, catH);
    imageMode(CENTER);
}

function draw() {
    image(cat, width / 2, height / 2, catW, catH);
    if (catH < cat.height) {
        catW++;
        catH++;
    }
}
