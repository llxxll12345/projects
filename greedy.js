<script type="text/javascript">
        //initializing styles and fashion!
        function $(str) {
	        return document.getElementById(str);
        } //get from document
        function $tag(str,target) {
	        target = target || document;
	        return target.getElementsByTagName(str);
        } //get from tag
        //generate a 2D array
        function multiArray(m, n) {
            var arr = new Array(n);
            for (var i = 0; i < m; i++)
                arr[i] = new Array(m);
            return arr;
        }
        //print info
        //get info
        function getText(target) {
            if (document.all) return target.innerText;
            else return target.textContent;
        }
        var std_v = 20;
        var width = 20;
        var height = 20;
	    var Exclaim = ["Good Job!","Excellent!","Amazing!","Extraodinary!","orz Lord!"];
        var len = 5;
	    var speed; 
	    var Grids = multiArray(width,height);
	    var map;
	    var snake;
	    var btnStart;
	    var topScore = len;
	    var snakeTimer; 
	    var brakeTimers = [];
	    var acceleratorTimers = [];
	    var directkey;
	   // btnPause.setAttribute("disabled", true);
        window.onload = function(){
	        btnStart = $("btnStart");
	        Create_Grid(); 
	        document.onkeydown = attachEvents; // attach to direction event
	        btnStart.onclick = function (e) {
	            btnStart.blur(); //blur focus
		        start(); //start game
		        btnStart.setAttribute("disabled", true);
		        //btnPause.removeAttribute("disabled");
		        btnStart.style.color = "#aaa"; //change of the starting button
		        //btnPause.style.color = "#fff";
	        }
        }
        //add objects
        function addObject(name){
            var p = pointGenerator();
            map[p[0]][p[1]] = name;
            Grids[p[0]][p[1]].className = name;
        }
        function add_ba(){
            var num = numGenerator(1, 5);
            for (var i = 1; i <= num; i++){
                brakeTimers.push(window.setTimeout(function(){addObject("brake"),1000}));
                acceleratorTimers.push(window.setTimeout(function (){addObject("accelerator"), 1000}));//?
            }
        }
        //clear off
        function clear(){
            for (var y = 0; y < Grids.length; y++){
                for (var x = 0; x < Grids[y].length; x++){
                    Grids[x][y].className = "";
                }
            }
        }
        //generate a ramdom point
        function pointGenerator(startX, startY, endX, endY) {
            startX = startX || 0;
            startY = startY || 0;
            endX = endX || width;
            endY = endY || height;
            var temp = [];
            var x = Math.floor(Math.random() * (endX - startX)) + startX;
            var y = Math.floor(Math.random() * (endY - startY)) + startY;
            if (map[x][y]) 
                return pointGenerator(startX, startY, endX, endY);
            temp[0] = x;
            temp[1] = y;
            return temp;
        }
        //generate random numbers
        function numGenerator(start, end) {
            return Math.floor(Math.random() * (end - start)) + start;
        }
        //start the game
        function start() {
	        len = 3;
	        speed = 10;
	        directkey = 39;
	        map = multiArray(width,height);
	        snake = new Array();
	        clear();
	        Create_snake();
	        for (var i = 1; i <= 10;i ++)
	            addObject("food");
	        addObject("trap");
	        walk();
	        add_ba();
        }
        //Create Grids
        function Create_Grid(){
	        var body = $tag("body")[0];
	        var table = document.createElement("table");
		    var tbody = document.createElement("tbody")
	        for(var j = 0; j < height; j++){
		        var col = document.createElement("tr");
		        for(var i = 0; i < width; i++){
			        var row = document.createElement("td");
			        Grids[i][j] = col.appendChild(row);
		        }
		        tbody.appendChild(col);
	        }
	        table.appendChild(tbody);
	        $("snakeWrap").appendChild(table);
        }
        //Construct A Sanke
        function Create_snake(){
	        var pointer = pointGenerator(len-1, len-1, width/2);
	        for(var i = 0; i < len; i++) {
		        var x = pointer[0] - i,
			        y = pointer[1];
		        snake.push([x,y]);
		        map[x][y] = "cover";
	        }
        }
        //Add keyboard event
        function attachEvents(enter){
	        enter = enter  || event;
	        directkey = Math.abs(enter.keyCode - directkey) != 2 && enter.keyCode > 36 && enter.keyCode < 41 ? enter.keyCode : directkey;
	        return false;
        }
        //Timer of walking
        function walk(){
	        if(snakeTimer) window.clearInterval(snakeTimer);
	        snakeTimer = window.setInterval(move, Math.floor(3000 / speed));
        }
        //moving the snake
        function move(){
	        //get the target point
	        var headX = snake[0][0],
		        headY = snake[0][1];
	        switch(directkey){
		        case 37: headX = (headX - 1 + width) % width; break;
		        case 38: headY = (headY - 1 + height) % height; break;
		        case 39: headX = (headX + 1 + width) % width; break
	            case 40: headY = (headY + 1 + height) % height; break;
	        }
	        //meet itself or too short, end game
	        if (map[headX][headY] == "cover" || len <= 2) {
	            alert("GAME OVER >_<");
	            if (getText($("score")) * 1 < len) alert("Your Score is " + len * 10);
	            $("score").innerHTML = Math.max(getText($("score")), len * 10);
	            btnStart.removeAttribute("disabled");
	            btnStart.style.color = "#000"; //change Start button
	            window.clearInterval(snakeTimer); //
	            return;
	            for (var i = 0; i < brakeTimers.length; i++) window.clearTimeout(brakeTimers[i]);
	            for (var i = 0; i < acceleratorTimers.length; i++) window.clearTimeout(acceleratorTimers[i]);
	        }
	        //level up
	        if(len % 7 == 0 && speed < 60 && map[headX][headY] == "food") {
	            speed += 5;
	            //document.onkeydown = alert("Speed up! Avoid traps!\ _ /");
	            walk();
	            //document.onkeydown = attachEvents;
	        }
	        //slower, get a break
	        if(map[headX][headY] == "brake") {
	            speed = 5;
	            //document.onkeydown = alert("Slow down for a moment!~_~");
	            walk();
	            //document.onkeydown = attachEvents;
	            //attachEvents(enter);
	            //move();
	            
	        }
	        //Meet an accelerator
	        if(map[headX][headY] == "accelerator") {
	            speed += 20;
	            //console.log("You meet an accelerator!\ _ /");
	            walk();
	            //document.onkeydown = attachEvents;
	            //attachEvents(enter);
		        
	        }
	        //add Trap
	        if(len % 7 == 0 && len < 60 && map[headX][headY] == "food") {
		        addObject("trap");
	        }
	        //Excalim
	        //if(len <= 50 && len % 10 == 0){
		        //var cheer = Exclaim[len/10-1];
		       // trace(cheer);
	        //}
	        //Eat and gain length
	        if(map[headX][headY] != "food"){
	            var lastX = snake[snake.length-1][0];
			    var lastY = snake[snake.length-1][1];
		        map[lastX][lastY] = false;
		        Grids[lastX][lastY].className = "";
		        snake.pop();
	        }else{
		        map[headX][headY] = false;
		        //trace("Gain food!");
		        addObject("food");
	        }
            //meet traps and lose length
	        if (map[headX][headY] == "trap"){
	            var lastX = snake[snake.length - 1][0];
	            var lastY = snake[snake.length - 1][1];
	            map[lastX][lastY] = false;
	            Grids[lastX][lastY].className = "";
	            snake.pop();
	            //trace("Oh no!You meet a trap!");
	        }
	        snake.unshift([headX, headY]);
	        map[headX][headY] = "cover";
	        Grids[headX][headY].className = "cover";
	        len = snake.length;
        }
        /*function Pause(obj, mytime) {
            if (window.eventList == Null) window.eventList = new Array();
            var index = -1;
            for (var i = 0; i < window.eventList.length; i++) {
                if (window.eventList[i] == null) {
                    window.eventList[i] = obj;
                    ind = i;
                    break;
                }
            }
            if (ind == -1) {
                ind = window.eventList.length;
                window.eventList[ind] = obj;
            }
            setTimeout(resume, mytime);
        }*/                                                                   
    </script>