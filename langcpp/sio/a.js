window.onscroll = function() {scroll_function()};

let canvashtml = document.body.children[0].children[0].children[2];

function randomHsl() {
    return 'hsla(' + (Math.random() * 360) + ', 100%, 50%, 1)';
}

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

canvas.width = 920;
canvas.height= 100;

let a = [];
let gap = 20;
let size = 5;
let spring = 0.005;
let damping = 0.05;
let init_disturbance = 20;

let max_x = canvas.width;
let max_y = canvas.height;

function get_random_color() {
	return "#" + ((1 << 24) * Math.random() | 0).toString(16).padStart(6, "0");
}

for (var i = 0; i < max_x; i += gap) {
    for (var j = 0; j < max_y; j += gap) {
        a.push([i, j, i, j, init_disturbance * Math.random(), init_disturbance * Math.random(), 0, 0, get_random_color()]) 
    }
}

b = [
	[20, 0, 20, 0],
	[40, 0, 40, 0],
	[0, 20, 0, 20],
	[20, 40, 20, 40],
	[40, 40, 40, 40],
	[60, 60, 60, 60],
	[40, 80, 40, 80],
	[20, 80, 20, 80],

	[100, 0, 100, 0],
	[120, 0, 120, 0],
	[140, 0, 140, 0],
	[160, 0, 160, 0],

	[120, 20, 120, 20],
	[140, 20, 140, 20],
	[120, 40, 120, 40],
	[140, 40, 140, 40],
	[120, 60, 120, 60],
	[140, 60, 140, 60],
	[120, 80, 120, 80],
	[140, 80, 140, 80],
		[100, 80, 100, 80],

		[160, 80, 160, 80],

]

b.forEach((elem) => {
	elem.push(init_disturbance * Math.random(), init_disturbance * Math.random(), 0, 0, get_random_color());

	
})

b = a;

function draw() {
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);


        b.forEach(function(point){

			ctx.beginPath();

			point[6] = ((point[0] - point[2]) * -spring) - damping * point[4];
            point[7] = ((point[1] - point[3]) * -spring) - damping * point[5];

            point[4] += point[6];
            point[5] += point[7];

            point[0] += point[4];
            point[1] += point[5];

            ctx.rect(point[0], point[1], size, size);
            ctx.fillStyle = point[8];
			//ctx.fillStyle = '#FC6C85';
            ctx.fill();
        });

}

setInterval(draw, 30);
