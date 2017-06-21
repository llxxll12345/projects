
var chessboard = new Chessboard(15, 15);
var neu = new neuron();
var chessboardDom = $('.chessboard');

var t = 0, tick;
var hintcount = 0;
var boardstack = [];

var initData = function () {
    for (var i = 0; i < chessboard.row; i++) {
        var rowDom = $('<div></div>').addClass('roww');
        for (var j = 0; j < chessboard.column; j++) {
            var tile = $('<div></div>').addClass('tile').data({
                row: i,
                column: j
            });
            rowDom.append(tile);
        }
        chessboardDom.append(rowDom);
    }
};

var initEvent = function () {
    console.log("initevent!");
    $('.tile').on('click', function () {
        //chessboard.getdata();
        if (!chessboard.isEnded()) {
            var self = $(this);
            $('.hinter').removeClass('chess chess-max hinter');
            $('#mess1').attr('class', 'alert alert-success');
            $('#mess2').attr('class', 'text-info h3');
            $("#mess1").text("Click to start!");
            $("#mess2").text("You've got " + (5 - hintcount) + " chances to use hint!");
            console.log(self.is('.chess'));
            if (self.is('.chess')) {
                $('#mess1').attr('class', 'alert alert-warning');
                $("#mess1").text("Illegal movement!");
            } else {
                var row = self.data('row'), column = self.data('column');
                chessboard.put(row, column, Chessboard.MAX);
                boardstack.push(chessboard);
                self.addClass('chess chess-max current').text('x');
                console.log("MAX: " + row + ", " + column);

                if (!tick) {
                    tick = setInterval(function () {
                        t++;
                        $('.timer').text('Game lasted for ' + t + ' s');
                    }, 1000);
                }
               
                if (chessboard.isMaxWin()) {
                    chessboard.getdata();
                    neu.changeweight(boardstack, false);
                    chessboard.end();
                    clearInterval(tick);
                    //console.log(1);
                    $("#mess2").text('You spent ' + t + ' secondes to defeat the computer! GOOD JOB!');
                    return;
                }
               
                if (chessboard.isEnded()) {
                    clearInterval(tick);
                    $("#mess2").text('You spent ' + t + ' secondes to get into a draw with the computer.');
                    return;
                } else {
                    setTimeout(function () {
                        //var alpha = 0;
                        console.time('min');
                        var res = min(chessboard, 2, null, neu);
                        console.timeEnd('min');
                       
                        chessboard.put(res.row, res.column, Chessboard.MIN);
                        boardstack.push(chessboard);
                        $('.current').removeClass('current');
                        chessboardDom.find('.roww').eq(res.row).find('.tile').eq(res.column).addClass('chess chess-min current').text('o');
                        console.log("MIN: " + res.row + ", " + res.column);

                        if (chessboard.isMinWin()) {
                            neu.changeweight(boardstack, true);
                            chessboard.end();
                            clearInterval(tick);
                            //console.log(2);
                            $("#mess2").text('You are defeated! HAHA :)');
                            return;
                        }
                     
                        if (chessboard.isEnded()) {
                            clearInterval(tick);
                            neu.changeweight(boardstack, false);
                            //console.log(3);
                            $("#mess2").text('You spent ' + t + ' secondes to defeat the computer! GOOD JOB!');
                            return;
                        }
                    }, 200);
                }
            }
        }
    });
    $('.hint').on('click', function () {
        var s = "1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1";
        setTimeout(function () {
            if (hintcount <= 4 && !chessboard.isEnded()) {
                hintcount++;
                console.time('max');
                //var beta = 0;
                var res = max(chessboard, 2, null, neu);
                console.timeEnd('max');
                chessboardDom.find('.roww').eq(res.row).find('.tile').eq(res.column).addClass('chess chess-max hinter');
                //$('.hinter').removeClass('hinter');
                console.log("Hint: " + res.row + ", " + res.column);
            }
            else if (chessboard.isEnded()) {
                $('#mess2').attr('class', 'alert alert-warning h3');
                $("#mess2").text("The game has ended!")
            }
            else {
                $('#mess2').attr('class', 'alert alert-warning h3');
                $("#mess2").text("You can use at most five hints!");
            }
        }, 200);
    });
    $('#roll').on('click', function () {

        console.log("clicked");
        var steps = chessboard.rollback(2);
        
        steps.forEach(function (step) {
            chessboardDom.find('.roww').eq(step.row).find('.tile').eq(step.column).removeClass('chess chess-min chess-max current hinter').text('');
        });
     
        var step = chessboard.current();
        if (step) {
            chessboardDom.find('.roww').eq(step.row).find('.tile').eq(step.column).addClass('current');
        }
    });
};

var restart = function () {
    $('.restart').on('click', function () {
        $('#input').removeClass('input1');
        if (chessboard.isEnded()) {
            chessboard.changestatus();
            for (var i = 0; i < chessboard.row; i++) {
                    for (var j = 0; j < chessboard.column; j++) {
                        console.log(i);
                        chessboardDom.find('.roww').eq(i).find('.tile').eq(j).removeClass('chess chess-min chess-max current hinter').text('');
                    }
                }
                console.log("restart!");
                t = 0;
                tick = null;
                hintcount = 0;
                chessboard = new Chessboard(15, 15);
                initEvent();
        }
        else {
            alert("No yet ended~!");
            //console.log("unended restart exception");
        }
    });
};


initData();
initEvent();
restart();