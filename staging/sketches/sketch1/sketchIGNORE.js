// Sample solution (delete from autograder)

function setup() {
    createCanvas(400, 400);
}

function draw() {
    background(0);
    fill(255);
    circle(width / 2, height / 2, 50);
}

function deleteMe() {
    var a = "a"
    if (10 == "10") {
        console.log("true")
    }
    return 1
}

// To ignore
// no-unused-vars (makes things like setup() and error mecause they're not called)
// no-undef (marks things like createCanvas() as undefined)