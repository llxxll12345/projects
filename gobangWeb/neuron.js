var neuron = function () {
    this.weight = [];
    this.weight1 = [];
    this.inputval = [];
    this.midval = [];
    this.outputval;
    this.learnrate = 0.5;
    for (var i = 0; i < 14;i++){
        this.weight[i] = [];
        this.data = [];
        for (var j = 0; j < 7;j++){
            this.weight[i][j] = 10;
            this.weight1[i] = 5;
        }
    }
}

neuron.prototype.changeweight = function (step, win) {
    var expectedvalue;
    var stepnum = step.length;
    stepnum--;

    if (win == true) {
        expectedvalue = 1;
    }
    else {
        expectedvalue = -1;
    }
    while (stepnum >= 0) {
        this.getinput(step[stepnum]);
        //console.log(step[stepnum].getdata().toString());
        this.getoutput().val;
        console.log("stepn " + stepnum + "val " + this.getoutput().val);
        this.feedback(expectedvalue);
        expectedvalue = this.getoutput().val;
        stepnum--;
    }
    var str = "";
    for (var i = 0; i < 14; i++) {
        for (var j = 0; j < 7; j++) {
            console.log("weight ", i, " ", j, " ", this.weight[i][j]);
            str += "weight " + i + " " + j + ":" + this.weight[i][j] + " "; 
            console.log("weight1", j, " ", this.weight1[j]);
            str += "weight1 " + j + ":" + this.weight1[j] + "  ";
        }
    }
    document.getElementById("input").value = str;
    $('#input').addClass('input1');
};

neuron.prototype.getinput = function (board) {
    var dat = board.getdata();
    for (var i = 0; i < 7; i++){
        this.inputval[i] = board.analyseMax(board.getdata(), i + 1);
        this.inputval[i + 7] = board.analyseMin(board.getdata(), i + 1);
    }
    var sum = 0;
    for (var i = 0; i < 14; i++) {
        sum += this.inputval[i];
    }
    for (var i = 0; i < 14; i++) {
        this.inputval[i] = 0 | this.inputval[i] / sum;
    }
}

neuron.prototype.getoutput = function () {
    for (var i = 0; i < 7; i++) {
        this.midval[i] = 0;
        for (var j = 0; j < 7; j++) {
            this.midval[i] += this.weight[j][i] * this.inputval[j];
        }
        this.outputval = 0;
        for (var j = 0; j < 7;j++){
            this.outputval += this.midval[j] * this.weight1[j];
            //console.log("output " + this.midval[j] * this.weight1[j]);
        }
    }
    //console.log("output " +this.outputval);
    return {
        val: this.outputval
    };
}

neuron.prototype.feedback = function (goal) {
    for (var i = 0; i < 14;i ++) {
        for (var j = 0; j < 7; j++) {
            this.weight[i][j] = this.learnrate * 1.0 / (1.0 + Math.pow(Math.exp, (- this.getoutput().val + goal) * (this.inputval[i])));
        }
    }
    for (i = 0; i < 7; i++) {
        this.weight1[i] = this.learnrate * 1.0 / (1.0 + Math.pow(Math.exp, (- this.getoutput().val + goal) * (this.midval[i])));
    }
};

/*var read = function () {

};

var write = function () {

};*/
