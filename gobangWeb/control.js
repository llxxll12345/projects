var Chessboard = function (row, column) {
    this.data = [];
    this.row = row;
    this.column = column;
    this.wins = [];
    this.count = 0;
    this.maxWin = [];
    this.minWin = [];
    //initialize
    for (var i = 0; i < row; i++) {
        this.data[i] = [];
        this.wins[i] = [];
        for (var j = 0; j < column; j++) {
            this.data[i][j] = Chessboard.NONE;
            this.wins[i][j] = [];
        }
    }

    for (var i = 0; i < row; i++) {
        for (var j = 0; j <= column - 5; j++) {
            for (var k = 0; k < 5; k++) {
                this.wins[i][j + k][this.count] = true;
            }
            this.count++;
        }
    }

    for (var i = 0; i < column; i++) {
        for (var j = 0; j <= row - 5; j++) {
            for (var k = 0; k < 5; k++) {
                this.wins[j + k][i][this.count] = true;
            }
            this.count++;
        }
    }

    for (var i = 0; i <= row - 5; i++) {
        for (var j = 0; j <= column - 5; j++) {
            for (var k = 0; k < 5; k++) {
                this.wins[i + k][j + k][this.count] = true;
            }
            this.count++;
        }
    }

    for (var i = 0; i <= row - 5; i++) {
        for (var j = column - 1; j >= 4; j--) {
            for (var k = 0; k < 5; k++) {
                this.wins[i + k][j - k][this.count] = true;
            }
            this.count++;
        }
    }

    for (var i = 0; i < this.count; i++) {
        this.maxWin[i] = {
            max: 0,
            min: 0
        };
        this.minWin[i] = {
            min: 0,
            max: 0
        };
    }

    this.stack = [];

    this.is_ended = false;
};

Chessboard.prototype.changestatus = function(){
    this.is_ended = false;
};

Chessboard.prototype.toString = function () {
    return this.data.map(function (data) {
        return data.toString();
    }).join('\n');
};

Chessboard.prototype.current = function () {
    var l = this.stack.length;
    if (l) {
        return this.stack[l - 1];
    }
};

Chessboard.prototype.getstack = function () {
    return this.stack;
};
Chessboard.prototype.getdata = function () {
    return this.data;
}
Chessboard.prototype.put = function (row, column, type) {
    if (this.data[row][column] == Chessboard.NONE) {
        this.data[row][column] = type;

        this.stack.push({
            row: row,
            column: column,
            type: type
        });

        for (var i = 0; i < this.count; i++) {
            if (this.wins[row][column][i]) {
                if (type == Chessboard.MAX) {
                    this.maxWin[i].max++;
                    this.minWin[i].max++;
                } else {
                    this.minWin[i].min++;
                    this.maxWin[i].min++;
                }
            }
        }

        if (this.stack.length == this.row * this.column) {
            this.end();
        }
    }
    return this;
};

Chessboard.prototype.rollback = function (n) {

    var steps = [];
    n = n || 1;
    for (var i = 0; i < n; i++) {
        var step = this.stack.pop();
        if (step) {
            steps.push(step);
            var row = step.row,
                column = step.column,
                type = step.type;

            this.data[row][column] = Chessboard.NONE;
            for (var j = 0; j < this.count; j++) {
                if (this.wins[row][column][j]) {
                    if (type == Chessboard.MAX) {
                        this.maxWin[j].max--;
                        this.minWin[j].max--;
                    } else {
                        this.minWin[j].min--;
                        this.maxWin[j].min--;
                    }
                }
            }
        }
    }
    this.is_ended = false;
    return steps;
};

Chessboard.prototype.getNearPoints = function (p) {
    var points = [],
        row, column;
    for (var i = -2; i <= 2; i++) {

        row = p.row + i;
        column = p.column + i;
        if (this.isValid(row, column)) {
            points.push({
                row: row,
                column: column
            });
        }

        row = p.row - i;
        column = p.column + i;
        if (this.isValid(row, column)) {
            points.push({
                row: row,
                column: column
            });
        }

        row = p.row;
        column = p.column - i;
        if (this.isValid(row, column)) {
            points.push({
                row: row,
                column: column
            });
        }

        row = p.row - i;
        column = p.column;
        if (this.isValid(row, column)) {
            points.push({
                row: row,
                column: column
            });
        }
    }
    return points;
};

Chessboard.prototype.isValid = function (row, column) {
    return row >= 0 && row < this.row && column >= 0 && column < this.column && this.data[row][column] == Chessboard.NONE;
};

Chessboard.prototype.availableSteps = function () {
    var availableSteps = [],
        row = this.row,
        column = this.column,
        stackLen = this.stack.length,
        centerRow = Math.floor((row - 1) / 2),
        centerColumn = Math.floor((column - 1) / 2);
    if (!stackLen || (stackLen == 1 && this.data[centerRow][centerColumn] == Chessboard.NONE)) {
        availableSteps.push({
            row: centerRow,
            column: centerColumn
        });
        return availableSteps;
    } else {
        if (stackLen == 1) {
            var nextRow = centerRow + (Math.random() < 0.5 ? -1 : 1),
                nextColumn = centerColumn + (Math.random() < 0.5 ? -1 : 1);
            availableSteps.push({
                row: nextRow,
                column: nextColumn
            });
            return availableSteps;
        } else {
            var hash = {};
            this.stack.forEach(function (p) {
                nearPoints = this.getNearPoints(p);
                nearPoints.forEach(function (nearPoint) {
                    var row = nearPoint.row,
                        column = nearPoint.column;
                    if (!hash[row + '#' + column]) {
                        availableSteps.push(nearPoint);
                        hash[row + '#' + column] = true;
                    }
                });
            }.bind(this));
            return availableSteps;
        }
    }
    return availableSteps;
};

Chessboard.prototype.analyseMax = function (data, type) {
    //console.log("analysing MAX!");
    data = data.toString();
    switch (type) {
        case Chessboard.FIVE:
            return ~data.indexOf('1,1,1,1,1') ? 1 : 0;
        case Chessboard.AFOUR:
            if (~data.indexOf('0,1,1,1,1,0')) {
                return 1;
            }
            return 0;
        case Chessboard.FOUR:
            var c = 0;
            var res1 = data.match(/2,1,1,1,1,0/g);
            var res2 = data.match(/0,1,1,1,1,2/g);
            var res3 = data.match(/1,0,1,1,1/g);
            var res4 = data.match(/1,1,0,1,1/g);
            var res5 = data.match(/1,1,1,0,1/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            c += (res4 ? res4.length : 0);
            c += (res5 ? res5.length : 0);
            return c;
        case Chessboard.ATHREE:
            var c = 0;
            var res1 = data.match(/0,1,1,1,0/g);
            var res2 = data.match(/0,1,1,0,1,0/g);
            var res3 = data.match(/0,1,0,1,1,0/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            return c;
        case Chessboard.THREE:
            var c = 0;
            var res1 = data.match(/2,1,1,1,0,0/g);
            var res2 = data.match(/0,0,1,1,1,2/g);
            var res3 = data.match(/2,1,1,0,1,0/g);
            var res4 = data.match(/0,1,0,1,1,2/g);
            var res5 = data.match(/2,1,0,1,1,0/g);
            var res6 = data.match(/0,1,1,0,1,2/g);
            var res7 = data.match(/1,0,0,1,1/g);
            var res8 = data.match(/1,1,0,0,1/g);
            var res9 = data.match(/1,0,1,0,1/g);
            var res10 = data.match(/2,0,1,1,1,0,2/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            c += (res4 ? res4.length : 0);
            c += (res5 ? res5.length : 0);
            c += (res6 ? res6.length : 0);
            c += (res7 ? res7.length : 0);
            c += (res8 ? res8.length : 0);
            c += (res9 ? res9.length : 0);
            c += (res10 ? res10.length : 0);
            return c;
        case Chessboard.ATWO:
            var c = 0;
            var res1 = data.match(/0,0,1,1,0,0/g);
            var res2 = data.match(/0,1,0,1,0/g);
            var res3 = data.match(/0,1,0,0,1,0/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            return c;
        case Chessboard.TWO:
            var c = 0;
            var res1 = data.match(/0,0,1,1,0,0/g);
            var res2 = data.match(/0,1,0,1,0/g);
            var res3 = data.match(/0,1,0,0,1,0/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            return c;
        default:
            return 0;
    }
};

Chessboard.prototype.analyseMin = function (data, type) {
    //console.log("analysing MAX!");
    data = data.toString();
    //console.log("data:" + data);
    var res = [];
    switch (type) {
        case Chessboard.FIVE:
            return ~data.indexOf('2,2,2,2,2') ? 1 : 0;
        case Chessboard.AFOUR:
            if (~data.indexOf('0,2,2,2,2,0')) {
                return 1;
            }
            return 0;
        case Chessboard.FOUR:
            var c = 0;
            var res1 = data.match(/1,2,2,2,2,0/g);
            var res2 = data.match(/0,2,2,2,2,1/g);
            var res3 = data.match(/2,0,2,2,2/g);
            var res4 = data.match(/2,2,0,2,2/g);
            var res5 = data.match(/2,2,2,0,2/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            c += (res4 ? res4.length : 0);
            c += (res5 ? res5.length : 0);
            return c;
        case Chessboard.ATHREE:
            var c = 0;
            var res1 = data.match(/0,2,2,2,0/g);
            var res2 = data.match(/0,2,2,0,2,0/g);
            var res3 = data.match(/0,2,0,2,2,0/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            return c;
        case Chessboard.THREE:
            var c = 0;
            var res1 = data.match(/1,2,2,2,0,0/g);
            var res2 = data.match(/0,0,2,2,2,1/g);
            var res3 = data.match(/1,2,2,0,2,0/g);
            var res4 = data.match(/0,2,0,2,2,1/g);
            var res5 = data.match(/1,0,2,0,2,2,0/g);
            var res6 = data.match(/0,2,2,0,2,1/g);
            var res7 = data.match(/2,0,0,2,2/g);
            var res8 = data.match(/2,2,0,0,2/g);
            var res9 = data.match(/2,0,2,0,2/g);
            var res10 = data.match(/1,0,2,2,2,0,1/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            c += (res4 ? res4.length : 0);
            c += (res5 ? res5.length : 0);
            c += (res6 ? res6.length : 0);
            c += (res7 ? res7.length : 0);
            c += (res8 ? res8.length : 0);
            c += (res9 ? res9.length : 0);
            c += (res10 ? res10.length : 0);
            return c;
        case Chessboard.ATWO:
            var c = 0;
            var res1 = data.match(/0,0,2,2,0,0/g);
            var res2 = data.match(/0,2,0,2,0/g);
            var res3 = data.match(/0,2,0,0,2,0/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            return c;
        case Chessboard.TWO:
            var c = 0;
            var res1 = data.match(/0,0,1,1,0,0/g);
            var res2 = data.match(/0,1,0,1,0/g);
            var res3 = data.match(/0,1,0,0,1,0/g);
            c += (res1 ? res1.length : 0);
            c += (res2 ? res2.length : 0);
            c += (res3 ? res3.length : 0);
            return c;
        default:
            return 0;
    }
};

Chessboard.prototype.evaluate = function () {
    var maxW = minW = 0;
    var maxGroup = {
        "5": 0,
        "4": 0,
        "3": 0,
        "2": 0,
        "1": 0
    },
    minGroup = {
        "5": 0,
        "4": 0,
        "3": 0,
        "2": 0,
        "1": 0
    };
    for (var i = 0; i < this.count; i++) {
        if (this.maxWin[i].max == 5 && !this.maxWin[i].min) {
            return Chessboard.MAX_VALUE;
        }
        if (this.minWin[i].min == 5 && !this.minWin[i].max) {
            return Chessboard.MIN_VALUE;
        }
        if (this.maxWin[i].max == 4 && !this.maxWin[i].min) {
            maxGroup[4]++;
        }
        if (this.minWin[i].min == 4 && !this.minWin[i].max) {
            minGroup[4]++;
        }
        if (this.maxWin[i].max == 3 && !this.maxWin[i].min) {
            maxGroup[3]++;
        }
        if (this.minWin[i].min == 3 && !this.minWin[i].max) {
            minGroup[3]++;
        }
        if (this.maxWin[i].max == 2 && !this.maxWin[i].min) {
            maxGroup[2]++;
        }
        if (this.minWin[i].min == 2 && !this.minWin[i].max) {
            minGroup[2]++;
        }
        if (this.maxWin[i].max == 1 && !this.maxWin[i].min) {
            maxGroup[1]++;
        }
        if (this.minWin[i].min == 1 && !this.minWin[i].max) {
            minGroup[1]++;
        }
    }
    maxW = maxGroup[4] * Chessboard.FOURV + maxGroup[3] * Chessboard.THREEV + maxGroup[2] * Chessboard.TWOV + maxGroup[1] * Chessboard.ONEV;
    minW = minGroup[4] * Chessboard.FOURV + minGroup[3] * Chessboard.THREEV + minGroup[2] * Chessboard.TWOV + minGroup[1] * Chessboard.ONEV;
    return maxW - minW;
};

Chessboard.prototype.isMaxWin = function () {
    var w = this.evaluate();
    return w >= Chessboard.MAX_VALUE ? true : false;
};

Chessboard.prototype.isMinWin = function () {
    var w = this.evaluate();
    return w <= Chessboard.MIN_VALUE ? true : false;
};

Chessboard.prototype.end = function () {
    this.is_ended = true;
    return this;
};

Chessboard.prototype.isEnded = function () {
    return this.is_ended;
};

var max = function (currentChessboard, depth, beta, neu) {
    var row, column, alpha = -Infinity;
    neu.getinput(currentChessboard);
    var neuval = neu.getoutput();
    if (depth == 0) {
        alpha = currentChessboard.evaluate();
        return {
            w: alpha
        };
    } else {
        var steps = currentChessboard.availableSteps();
        if (steps.length) {
            for (var i = 0, l = steps.length; i < l; i++) {
                var step = steps[i];
                currentChessboard.put(step.row, step.column, Chessboard.MAX);
                if (currentChessboard.isMaxWin()) {
                    alpha = Chessboard.MAX_VALUE;
                    row = step.row;
                    column = step.column;
                    currentChessboard.rollback();
                    break;
                } else {
                    var res = min(currentChessboard, depth - 1, alpha, neu) || {
                        w: currentChessboard.evaluate() + neuval.val
                    };
                    currentChessboard.rollback();
                    if (res.w > alpha) {
                        alpha = res.w;
                        row = step.row;
                        column = step.column;
                    }
                    if (alpha >= beta) {
                        //console.log('max node in total ' + l + ' situations£¬cut ' + (l - 1 - i) + ' min situations in total');
                        break;
                    }
                }
            }
            return {
                w: alpha,
                row: row,
                column: column
            };
        }
    }
};

var min = function (currentChessboard, depth, alpha, neu) {
    var row, column, beta = Infinity;
    neu.getinput(currentChessboard);
    var neuval = neu.getoutput();
    if (depth == 0) {
        beta = currentChessboard.evaluate();
        return {
            w: beta
        };
    } else {
        var steps = currentChessboard.availableSteps();
        console.log('search MIN ' + steps.length + ' situations');
        if (steps.length) {

            for (var i = 0, l = steps.length; i < l; i++) {
                var step = steps[i];

                currentChessboard.put(step.row, step.column, Chessboard.MIN);

                if (currentChessboard.isMinWin()) {
                    beta = Chessboard.MIN_VALUE;
                    row = step.row;
                    column = step.column;

                    currentChessboard.rollback();
                    break;
                } else {
                    var res = max(currentChessboard, depth - 1, beta, neu) || {
                        w: currentChessboard.evaluate() + neuval.val
                    };

                    currentChessboard.rollback();
                    if (res.w < beta) {

                        beta = res.w;
                        row = step.row;
                        column = step.column;
                    }

                    if (beta <= alpha) {
                        //console.log('MIN node in total' + l + ' situations, cut ' + (l - 1 - i) + ' MAX situations');
                        break;
                    }
                }
            }
            return {
                w: beta,
                row: row,
                column: column
            };
        }
    }
};

Chessboard.NONE = 0;
Chessboard.MAX = 1;
Chessboard.MIN = 2;
Chessboard.FIVE = 1;
Chessboard.AFOUR = 2;
Chessboard.FOUR = 3;
Chessboard.ATHREE = 4;
Chessboard.THREE = 5;
Chessboard.ATWO = 6;
Chessboard.TWO = 7;

Chessboard.MAX_VALUE = 100000;
Chessboard.MIN_VALUE = -100000;
Chessboard.FIVEV = 100000;
Chessboard.AFOURV = 10000;
Chessboard.FOURV = 5000;
Chessboard.ATHREEV = 2000;
Chessboard.THREEV = 1000;
Chessboard.ATWOV = 500;
Chessboard.TWOV = 200;
Chessboard.ONEV = 10;
