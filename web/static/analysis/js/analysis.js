// 传输层分析
// function table1x() {
//     $.ajax({
//         url: "/table1/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {

//             $('#table1').empty("");
//             $.each(list, function (i,n){
//                 $('#table1').append($("<tr><td>"+n[6]+"</td><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+ n[2]+
//                     "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+"</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table1x, 1000);

// table1x();可行的
// function table1x() {
//     $.ajax({
//         url: "/table1/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             // 清空表格
//             $('#table1').empty();

//             // 滚动显示前 7 列内容，最多显示 10 行
//             let index = 0;
//             setInterval(() => {
//                 $('#table1').empty();
//                 for (let i = 0; i < 10; i++) {
//                     let rowIndex = (index + i) % list.length;
//                     let row = list[rowIndex];
//                     $('#table1').append($("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" + row[5] + "</td><td>" + row[6] + "</td></tr>"));
//                 }
//                 index = (index + 1) % list.length;
//             }, 2000); // 每 2 秒滚动一次
//         },
//         error: function (error) {
//             console.error('Error fetching data:', error);
//         }
//     });
// }

// table1x();

// function table1x() {
//     $.ajax({
//         url: "/table1/", // 别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             // 清空表格之前的内容
//             let index = 0;
//             let interval = setInterval(() => {
//                 // 只清空并添加新行，而不是每次都清空整个表格
//                 $('#table1').empty();
                
//                 // 通过 index 和 list 长度来动态添加数据
//                 for (let i = 0; i < 10; i++) {
//                     let rowIndex = (index + i) % list.length;
//                     let row = list[rowIndex];
//                     $('#table1').append($("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" + row[5] + "</td><td>" + row[6] + "</td></tr>"));
//                 }

//                 // 更新 index，确保数据滚动
//                 index = (index + 1) % list.length;
//             }, 1000); // 每 1 秒滚动一次
//         },
//         error: function (error) {
//             console.error('Error fetching data:', error);
//         }
//     });
// }

// table1x();
function table1x() {
    $.ajax({
        url: "/table1/",
        type: "GET",
        success: function (list) {
            if (list.length === 0) {
                console.error("No data received!");
                return;
            }

            // 初始化表格，只创建 10 行占位
            for (let i = 0; i < 10; i++) {
                $('#table1').append(
                    $("<tr id='row" + i + "'><td></td><td></td><td></td><td></td><td></td><td></td></tr>")
                );
            }

            let index = 0;

            setInterval(() => {
                for (let i = 0; i < 10; i++) {
                    let rowIndex = (index + i) % list.length;
                    let row = list[rowIndex];

                    // 更新每行内容
                    $("#row" + i).html(
                        "<td>" + row[0] + "</td><td>" + row[1] + "</td><td>" +
                        row[2] + "</td><td>" + row[3] + "</td><td>" +
                        row[4] + "</td><td>" + row[5] + "</td>"
                    ).css('animation', 'none'); // 移除旧动画

                    // 触发重绘以应用新动画
                    void $("#row" + i)[0].offsetWidth;

                    // 应用新动画
                    $("#row" + i).css('animation', 'scroll 1s linear infinite');
                }

                // 更新 index
                index = (index + 1) % list.length;
            }, 1000);
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}
table1x();

//TopK分析
function table2x() {
    $.ajax({
        url: "/table2/",
        type: "GET",
        success: function (list) {
            if (list.length === 0) {
                console.error("No data received!");
                return;
            }

            // 清空表格
            $('#table2').empty();

            // 初始化表格，只创建 11 行占位
            for (let i = 0; i < 10; i++) {
                $('#table2').append(
                    $("<tr id='row2_" + i + "'><td></td><td></td><td></td><td></td><td></td><td></td></tr>")
                );
            }

            let index = 0;

            setInterval(() => {
                for (let i = 0; i < 10; i++) {
                    let rowIndex = (index + i) % list.length;
                    let item = list[rowIndex];

                    // 创建每行的 HTML
                    let rowHtml = "<td>" + item.rank + "</td><td>" + item.row[0] + "</td><td>" +
                        item.row[1] + "</td><td>" + item.row[2] + "</td><td>" +
                        item.row[3] + "</td><td>" + item.count + "</td>";

                    // 如果 rank 为 1，加粗并将字体颜色设为白色
                    if (item.rank === 1) {
                        rowHtml = "<td style='color: white;'><strong>" + item.rank + "</strong></td>" +
                                  "<td style='color: white;'><strong>" + item.row[0] + "</strong></td>" +
                                  "<td style='color: white;'><strong>" + item.row[1] + "</strong></td>" +
                                  "<td style='color: white;'><strong>" + item.row[2] + "</strong></td>" +
                                  "<td style='color: white;'><strong>" + item.row[3] + "</strong></td>" +
                                  "<td style='color: white;'><strong>" + item.count + "</strong></td>";
                    }

                    // 更新表格行内容
                    $("#row2_" + i).html(rowHtml);
                }

                // 更新 index
                index = (index + 1) % list.length;
            }, 1000); // 每 1 秒滚动一次
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

table2x();


//分位数估计
// 分位数估计
function table3x() {
    $.ajax({
        url: "/table3/",
        type: "GET",
        success: function (list) {
            if (list.length === 0) {
                console.error("No data received!");
                return;
            }

            // 清空表格
            $('#table3').empty();

            // 初始化表格，只创建 10 行占位
            for (let i = 0; i < 10; i++) {
                $('#table3').append(
                    $("<tr id='row3_" + i + "'><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>")
                );
            }

            let index = 0;

            setInterval(() => {
                $('#table3').empty();
                for (let i = 0; i < 10; i++) {
                    let rowIndex = (index + i) % list.length;
                    let row = list[rowIndex];

                    // 更新每行内容
                    $('#table3').append(
                        $("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" +
                        row[2] + "</td><td>" + row[3] + "</td><td>" +
                        row[4] + "</td><td>" + row[5] + "</td><td>" + row[6] + "</td></tr>")
                    );
                }

                // 更新 index
                index = (index + 1) % list.length;
            }, 1000); // 每 1 秒滚动一次
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

table3x();

//网络层分析
function table4x() {
    $.ajax({
        url: "/table4/", //别忘了加双引号
        type: "GET",
        success: function (list) {
            $('#table4').empty("");
            $.each(list, function (i,n){
                $('#table4').append($("<tr><td>"+n[6]+"</td><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+ n[2]+
                    "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+"</td></tr>"));
            });
        }
    })
}
setInterval(table4x, 1000);

numqiguai=0;
function mainTopx() {
    $.ajax({
        url: "/mainTop/", //别忘了加双引号
        type: "GET",
        success: function (list) {
            document.getElementById("mainTop1").innerText = list[0];
            document.getElementById("mainTop2").innerText = list[1];
            document.getElementById("mainTop3").innerText = Math.ceil(list[2]);
            
            if (Math.random() < 0.4 && numqiguai>10) {
                percentage = -1;
                numqiguai = (hashToPercentage(list[3])*percentage/100+numqiguai).toFixed(2);
                document.getElementById("mainTop4").innerText = numqiguai.toFixed(2);
            }else{
                (numqiguai = hashToPercentage(list[3])/100+numqiguai).toFixed(2);
                document.getElementById("mainTop4").innerText = numqiguai.toFixed(2);
            }

        }
    })
}
setInterval(mainTopx, 1000);

// 哈希函数
function hashToPercentage(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash % 101); // 映射到 0-100 的范围
}

//实时流量分析
function mainBottomx() {
    $.ajax({
        url: "/mainBottom/", //别忘了加双引号
        type: "GET",
        success: function (list) {
            var XData = [];
            var YData1 = [];
            var YData2 = [];
            var YData3 = [];
            $.each(list, function (i, n) {
                XData.push(n[0])
                YData1.push(n[1])
                YData2.push(n[2])
                YData3.push(n[3])
            });
            dataMainBottom = {
                "XData": XData,
                "YData1": YData1,
                "YData2": YData2,
                "YData3": YData3,
            };
            option = {
                tooltip: {trigger: 'axis', axisPointer: {lineStyle: {color: '#fff'}}},
                legend: {
                    icon: 'rect',
                    itemWidth: 12, itemHeight: 5, itemGap: 10,
                    data: ['总流量', '上行流量', '下行流量'],
                    right: '10px', top: '0px',
                    textStyle: {fontSize: 12, color: '#fff'}
                },
                grid: {x: 55, y: 35, x2: 30, y2: 90},
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,
                    axisLine: {lineStyle: {color: '#57617B'}},
                    axisLabel: {textStyle: {color: '#fff'}},
                    data: dataMainBottom.XData
                }],
                yAxis: [
                    {
                        type: 'value',
                        max : 250,
                        axisTick: {
                            show: false
                        },
                        axisLine: {lineStyle: {color: '#57617B'}},
                        axisLabel: {
                            margin: 10,
                            textStyle: {fontSize: 6},
                            textStyle: {color: '#fff'},
                            formatter: '{value}MB'
                        },
                        splitLine: {lineStyle: {color: '#57617B'}}
                    }, {
                        type: 'value',
                        max : 250,
                        axisTick: {
                            show: false
                        },
                        axisLine: {lineStyle: {color: '#57617B'}},
                        axisLabel: {
                            margin: 10,
                            textStyle: {fontSize: 9},
                            textStyle: {color: 'rgba(0,0,0,0)'},
                            formatter: '{value}MB'
                        },
                        splitLine: {lineStyle: {color: '#57617B'}}
                    }
                ],
                series: [
                    {
                        name: '总流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
                        yAxisIndex: 0,
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(122,234,19,0.3)'
                                }, {
                                    offset: 0.8,
                                    color: 'rgba(185,150,248,0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: {normal: {color: '#c40d44'}},
                        data: dataMainBottom.YData1
                    },
                    {
                        name: '上行流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
                        yAxisIndex: 1,
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(3, 194, 236, 0.3)'
                                }, {
                                    offset: 0.8,
                                    color: 'rgba(3, 194, 236, 0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: {normal: {color: '#03C2EC'}},
                        data: dataMainBottom.YData2
                    },
                    {
                        name: '下行流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
                        yAxisIndex: 1,
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(218, 57, 20, 0.3)'
                                }, {
                                    offset: 0.8,
                                    color: 'rgba(218, 57, 20, 0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: {normal: {color: '#DA3914'}},
                        data: dataMainBottom.YData3
                    }
                ]
            };
            var myChart = echarts.init(document.getElementById('mainBottom'));
            myChart.setOption(option);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            // 状态码
            console.log(XMLHttpRequest.status);
            // 状态
            console.log(XMLHttpRequest.readyState);
            // 错误信息
            console.log(textStatus);
        }
    })
}
setInterval(mainBottomx, 1000);


//流量读入
function readPcapx() {
    $.ajax({
        url: "/readCsv/", //别忘了加双引号
        type: "GET",
        success: function (list) {

        }
    })
}
setInterval(readPcapx, 1000);


// //行为分析与预测
// function behavior_input() {
//     $.ajax({
//         url: "/behavior_input/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//
//         }
//     })
// }
// setInterval(behavior_input(), 3000);
// setInterval(behavior_input, 3000);


