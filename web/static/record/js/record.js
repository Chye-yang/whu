function setDate(time, tt, isAdd) {
    var date = getCurTime(time);//也可以直接透传如'2021-5-8'
    var d = new Date(date);
    var t_s = d.getTime(); //转化为时间戳毫秒数
    var newt = new Date(date); //定义一个新时间
    if (isAdd) {
        newt.setTime(t_s + tt * 1000); //设置新时间比旧时间多五秒
    } else {
        newt.setTime(t_s - tt * 1000); //设置新时间比旧时间少五秒
    }
    newt = new Date(newt)
    var h = newt.getHours();
    var m = newt.getMinutes();
    var s = newt.getSeconds();
    return zeroPad(h) + ':' + zeroPad(m) + ':' + zeroPad(s);
}

function getCurTime(time) {
    var myDate = new Date();
    var nowYear = myDate.getFullYear();
    var nowMonth = myDate.getMonth() + 1;
    var nowDay = myDate.getDate();
    return nowYear + '-' + nowMonth + '-' + nowDay + ' ' + time;
}

function zeroPad(n) {
    return n < 10 ? '0' + n : n;
}

record_speed_number = []


function record_speed() {
    $.ajax({
        url: "/record_speed/",
        type: "GET",
        success: function (list) {
            var myChart = echarts.init(document.getElementById('lpeftmidbot'));

            var XData = [];
            var date = new Date();
            var now = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
            var t_s = date.getTime();
            var newt = new Date();
            if (record_speed_number.length > 0) {
                record_speed_number.shift();
                $.each(list, function (i, n) {
                    XData.push(setDate(now, 3 * (list.length - i - 1), false));
                    if (i === (record_speed_number.length)) {
                        record_speed_number.push(parseFloat(n));  // 确保数据是浮点数
                    }
                });
            } else {
                $.each(list, function (i, n) {
                    XData.push(setDate(now, 3 * (list.length - i - 1), false));
                    record_speed_number.push(parseFloat(n));  // 确保数据是浮点数
                });
            }

            option = {
                color: ['#d2d17c', '#7fd7b1', '#5578cf', '#5ebbeb', '#d16ad8', '#00b7ee', '#81dabe', '#5fc5ce'],
                backgroundColor: 'rgba(1,202,217,.2)',
                grid: {
                    left: 20,
                    right: 30,
                    top: 0,
                    bottom: 20
                },
                legend: {
                    top: 5,
                    textStyle: {
                        fontSize: 10,
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                grid: {
                    left: 20,
                    right: 30,
                    top: 40,
                    bottom: 10,
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.2)'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }
                    },
                    axisLabel: {
                        color: "rgba(255,255,255,.7)"
                    },
                    data: XData
                },
                yAxis: {
                    type: 'value',
                    min: 500,
                    max: 700,
                    interval: 20,
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.2)'
                        }
                    },
                    name: 'Mbps',
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }
                    },
                    axisLabel: {
                        color: "rgba(255,255,255,.7)"
                    },
                },
                series: [
                    {
                        type: 'line',
                        data: record_speed_number,
                        smooth: true,
                    }
                ]
            };
            myChart.setOption(option);
            window.addEventListener("resize", function () {
                myChart.resize();
            });
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
        }
    })
}
// function record_speed() {
//     $.ajax({
//         url: "/record_speed/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             // 初始化《网络流量回放速率》
//             var XData = [];
//             // var YData = ['100','102','104','106','108'];
//             var date = new Date();
//             var now = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
//             var t_s = date.getTime();
//             var newt = new Date();
//             if (record_speed_number.length > 0) {
//                 record_speed_number.shift()
//                 $.each(list, function (i, n) {
//                     XData.push(setDate(now, 3 * (list.length - i - 1), false));
//                     if (i === (record_speed_number.length)) {
//                         record_speed_number.push(n)
//                     }
//                 });
//             } else {
//                 $.each(list, function (i, n) {
//                     XData.push(setDate(now, 3 * (list.length - i - 1), false));
//                     record_speed_number.push(n)
//                 });
//             }
//             var myChart = echarts.init(document.getElementById('lpeftmidbot'));
//             option = {
//                 tooltip: {
//                     trigger: 'axis'
//                 },
//                 backgroundColor: 'rgba(1,202,217,.2)',
//                 grid: {
//                     left: 50,
//                     right: 20,
//                     top: 45,
//                     bottom: 30
//                 },
//                 legend: {
//                     top: 5,
//                     textStyle: {
//                         fontSize: 10,
//                         color: 'rgba(255,255,255,.7)'
//                     },
//                 },
//                 toolbox: {
//                     show: false,
//                     feature: {
//                         mark: {show: true},
//                         dataView: {show: true, readOnly: false},
//                         magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
//                         restore: {show: true},
//                         saveAsImage: {show: true}
//                     }
//                 },
//                 calculable: true,
//                 xAxis: [
//                     {
//                         type: 'category',
//                         axisLine: {
//                             lineStyle: {
//                                 color: 'rgba(255,255,255,.2)'
//                             }
//                         },
//                         splitLine: {
//                             lineStyle: {
//                                 color: 'rgba(255,255,255,.1)'
//                             }
//                         },
//                         axisLabel: {
//                             type: 'category',
//                             axisTick: {show: false},
//                             boundaryGap: false,
//                             textStyle: {
//                                 color: '#ccc',
//                                 fontSize: '12'
//                             },
//                             lineStyle: {
//                                 color: '#2c3459',
//                             },
//                             rotate: 0,
//                         },

//                         data: XData,
//                         axisPointer: {
//                             type: 'shadow'
//                         }
//                     }
//                 ],
//                 yAxis: [
//                     {
//                         type: 'value',
//                         min: 500,
//                         max: 700,
//                         interval: 20,
//                         axisLine: {
//                             lineStyle: {
//                                 color: 'rgba(255,255,255,.3)'
//                             }
//                         },
//                         name: 'Mbps',
//                         splitLine: {
//                             lineStyle: {
//                                 color: 'rgba(255,255,255,.01)'
//                             }
//                         }
//                     }

//                 ],
//                 series: [
//                     {
//                         type: 'line',
//                         smooth: true,
//                         itemStyle: {
//                             normal: {
//                                 color: '#f8e19a'
//                             }
//                         },
//                         data: record_speed_number
//                     }
//                 ]
//             };
//             myChart.setOption(option);
//             window.addEventListener("resize", function () {
//                 myChart.resize();
//             });
//         }, error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// }

speed_ping_number = []

function speed_ping() {
    $.ajax({
        url: "/record_ping/", //别忘了加双引号
        type: "GET",
        success: function (list) {
            // 初始化回放队列数目
            var myChart = echarts.init(document.getElementById('prbottom_box1'));

            var XData = [];
            // var YData = ['100','102','104','106','108'];
            var date = new Date();
            var now = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
            var t_s = date.getTime();
            var newt = new Date();
            if (speed_ping_number.length > 0) {
                speed_ping_number.shift()
                $.each(list, function (i, n) {
                    XData.push(setDate(now, 3 * (list.length - i - 1), false));
                    if (i === (speed_ping_number.length)) {
                        speed_ping_number.push(parseFloat(n))
                    }
                });
            } else {
                $.each(list, function (i, n) {
                    XData.push(setDate(now, 3 * (list.length - i - 1), false));
                    speed_ping_number.push(parseFloat(n))
                });
            }

            option = {
                color: ['#d2d17c', '#7fd7b1', '#5578cf', '#5ebbeb', '#d16ad8', '#f8e19a', '#00b7ee', '#81dabe', '#5fc5ce'],
                backgroundColor: 'rgba(1,202,217,.2)',
                grid: {
                    left: 20,
                    right: 30,
                    top: 0,
                    bottom: 20
                },
                legend: {
                    top: 5,

                    textStyle: {
                        fontSize: 10,
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                grid: {
                    left: 20,
                    right: 30,
                    top: 40,
                    bottom: 10,
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.2)'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }
                    },
                    axisLabel: {
                        color: "rgba(255,255,255,.7)"
                    },
                    data: XData
                },
                yAxis: {
                    type: 'value',
                    min: '90',
                    max: '100',
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.2)'
                        }
                    },
                    name: '%',
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        }
                    },
                    axisLabel: {
                        color: "rgba(255,255,255,.7)"
                    },
                },
                series: [
                    {
                        type: 'line',
                        data: speed_ping_number,
                        smooth: true,
                    }
                ]
            };
            myChart.setOption(option);

        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            // 状态码
            console.log(XMLHttpRequest.status);
            // 状态
            console.log(XMLHttpRequest.readyState);
            // 错误信息
            console.log(textStatus);
        }
    })
}

record_speed();
setInterval(record_speed, 3000);

speed_ping();
setInterval(speed_ping, 3000);
