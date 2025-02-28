// // 实时统计
// function real_time_statistics() {
//     $.ajax({
//         url: "/real_time_statistics/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             document.getElementById("all_behavior").innerText = list[0];
//             document.getElementById("normal_behavior").innerText = list[1];
//             document.getElementById("suspect_behavior").innerText = list[2];
//             document.getElementById("anomaly_behavior").innerText = list[3];
//             document.getElementById("all_behavior_predict").innerText = '(预测数：' + list[4] + ')';
//             document.getElementById("normal_behavior_predict").innerText = '(预测数：' + list[5] + ')';
//             document.getElementById("suspect_behavior_predict").innerText = '(预测数：' + list[6] + ')';
//             document.getElementById("anomaly_behavior_predict").innerText = '(预测数：' + list[7] + ')';
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// };
// setInterval(real_time_statistics(), 3000);
// setInterval(real_time_statistics, 3000);
//
// //协议分类
// function protocol_classification() {
//     $.ajax({
//         url: "/protocol_classification/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             var myChart = echarts.init(document.getElementById('echarts_1'));
//             var data = [
//                 {value: parseInt(list[0]), name: 'TCP'},
//                 {value: parseInt(list[1]), name: 'UDP'},
//                 {value: parseInt(list[2]), name: 'Other'}
//             ];
//             var data2 = [
//                 {value: parseInt(list[3]), name: 'TCP'},
//                 {value: parseInt(list[4]), name: 'UDP'},
//                 {value: parseInt(list[5]), name: 'Other'}
//             ];
//             option = {
//                 backgroundColor: 'rgba(0,0,0,0)',
//                 tooltip: {
//                     trigger: 'item',
//                     formatter: "{b}: <br/>{c} ({d}%)"
//                 },
//                 color: ['#25F3E6', '#F5C847', '#F84A4A'],
//                 legend: { //图例组件，颜色和名字
//                     x: '70%',
//                     y: 'center',
//                     orient: 'vertical',
//                     itemGap: 12, //图例每项之间的间隔
//                     itemWidth: 10,
//                     itemHeight: 10,
//                     icon: 'rect',
//                     data: ['TCP', 'UDP', 'Other'],
//                     textStyle: {
//                         color: [],
//                         fontStyle: 'normal',
//                         fontFamily: '微软雅黑',
//                         fontSize: 12,
//                     }
//                 },
//                 series: [{
//                     name: '',
//                     type: 'pie',
//                     clockwise: false, //饼图的扇区是否是顺时针排布
//                     minAngle: 20, //最小的扇区角度（0 ~ 360）
//                     center: ['35%', '50%'], //饼图的中心（圆心）坐标
//                     radius: [55, 80], //饼图的半径
//                     avoidLabelOverlap: true, ////是否启用防止标签重叠
//                     itemStyle: { //图形样式
//                         normal: {
//                             borderColor: '#1e2239',
//                             borderWidth: 2,
//                         },
//                     },
//                     label: { //标签的位置
//                         normal: {
//                             show: true,
//                             position: 'inside', //标签的位置
//                             formatter: "实时：{d}%",
//                             textStyle: {
//                                 color: '#fff',
//                             }
//                         },
//                         emphasis: {
//                             show: true,
//                             textStyle: {
//                                 fontWeight: 'bold'
//                             }
//                         }
//                     },
//                     data: data
//                 }, {
//                     name: '',
//                     type: 'pie',
//                     clockwise: false,
//                     silent: true,
//                     minAngle: 20, //最小的扇区角度（0 ~ 360）
//                     center: ['35%', '50%'], //饼图的中心（圆心）坐标
//                     radius: [0, 40], //饼图的半径
//                     itemStyle: { //图形样式
//                         normal: {
//                             borderColor: '#1e2239',
//                             borderWidth: 1.5,
//                             opacity: 0.9,
//                         }
//                     },
//                     label: { //标签的位置
//                         normal: {
//                             show: true,
//                             position: 'inside', //标签的位置
//                             formatter: "预测：{d}%",
//                             textStyle: {
//                                 color: '#fff',
//                                 fontSize: 10
//                             }
//                         },
//                         emphasis: {
//                             show: true,
//                             textStyle: {
//                                 fontWeight: 'bold'
//                             }
//                         }
//                     },
//                     data: data2
//                 }]
//             };
//             // 使用刚指定的配置项和数据显示图表。
//             myChart.setOption(option);
//             window.addEventListener("resize", function () {
//                 myChart.resize();
//             });
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// };
// setInterval(protocol_classification(), 3000);
// setInterval(protocol_classification, 3000);
//
// //行为分类
// function behavior_classification() {
//     $.ajax({
//         url: "/behavior_classification/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             var myChart = echarts.init(document.getElementById('echarts_5'));
//             var xData = ['文件传输', '邮件传输', '网络通讯', '网络管理', '其它'];
//             var data1 = [];
//             var data2 = [];
//             for (i = 0; i < xData.length; i++) {
//                 data1.push(parseInt(list[i]));
//                 data2.push(parseInt(list[i]) + parseInt(list[i + 5]));
//             }
//             option = {
//                 legend: {
//                     icon: 'rect',
//                     itemWidth: 14, itemHeight: 5, itemGap: 10,
//                     data: ['实时分析', '未来预测'],
//                     right: '10px', top: '0px',
//                     textStyle: {fontSize: 12, color: '#fff'},
//                     show:true
//                 },
//                 tooltip: {
//                     show: "true",
//                     trigger: 'item',
//                     backgroundColor: 'rgba(0,0,0,0.4)', // 背景
//                     padding: [8, 10], //内边距
//                     // extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影
//                     formatter: function (params) {
//                         if (params.seriesName != "") {
//                             return params.name + ' ：  ' + params.value + ' ';
//                         }
//                     },
//
//                 },
//                 grid: {
//                     borderWidth: 0,
//                     top: 20,
//                     bottom: 35,
//                     left: 55,
//                     right: 30,
//                     textStyle: {
//                         color: "#fff"
//                     }
//                 },
//                 xAxis: [{
//                     type: 'category',
//
//                     axisTick: {
//                         show: false
//                     },
//                     axisLine: {
//                         show: true,
//                         lineStyle: {
//                             color: '#363e83',
//                         }
//                     },
//                     axisLabel: {
//                         inside: false,
//                         textStyle: {
//                             color: '#bac0c0',
//                             fontWeight: 'normal',
//                             fontSize: '10',
//                         },
//                         // formatter:function(val){
//                         //     return val.split("").join("\n")
//                         // },
//                     },
//                     data: xData,
//                 }, {
//                     type: 'category',
//                     axisLine: {
//                         show: false
//                     },
//                     axisTick: {
//                         show: false
//                     },
//                     axisLabel: {
//                         show: false
//                     },
//                     splitArea: {
//                         show: false
//                     },
//                     splitLine: {
//                         show: false
//                     },
//                     data: xData,
//                 }],
//                 yAxis: {
//                     type: 'value',
//                     axisTick: {
//                         show: false
//                     },
//                     axisLine: {
//                         show: true,
//                         lineStyle: {
//                             color: '#32346c',
//                         }
//                     },
//                     splitLine: {
//                         show: true,
//                         lineStyle: {
//                             color: '#32346c ',
//                         }
//                     },
//                     axisLabel: {
//                         textStyle: {
//                             color: '#bac0c0',
//                             fontWeight: 'normal',
//                             fontSize: '12',
//                         },
//                         formatter: '{value}',
//                     },
//                 },
//                 series: [
//                     {
//                         name: '实时分析',
//                         type: 'bar',
//                         itemStyle: {
//                             normal: {
//                                 show: true,
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: '#00c0e9'
//                                 }, {
//                                     offset: 1,
//                                     color: '#3b73cf'
//                                 }]),
//                                 barBorderRadius: 50,
//                                 borderWidth: 0,
//                             },
//                             emphasis: {
//                                 shadowBlur: 15,
//                                 shadowColor: 'rgba(105,123, 214, 0.7)'
//                             }
//                         },
//                         zlevel: 2,
//                         barWidth: '20%',
//                         data: data1,
//                     },
//                     {
//                         name: '未来预测',
//                         type: 'bar',
//                         xAxisIndex: 1,
//                         zlevel: 1,
//                         itemStyle: {
//                             normal: {
//                                 show: true,
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: '#c42266'
//                                 }, {
//                                     offset: 1,
//                                     color: '#f1082b'
//                                 }]),
//                                 barBorderRadius: 50,
//                                 borderWidth: 0,
//                             },
//                             emphasis: {
//                                 shadowBlur: 15,
//                                 shadowColor: 'rgba(105,123, 214, 0.7)'
//                             }
//                         },
//                         barWidth: '20%',
//                         data: data2
//                     }
//                 ]
//             }
//             // 使用刚指定的配置项和数据显示图表。
//             myChart.setOption(option);
//             window.addEventListener("resize", function () {
//                 myChart.resize();
//             });
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// };
// setInterval(behavior_classification(), 3000);
// setInterval(behavior_classification, 3000);
//
// //流量大小实时分析与预测
//
// flow_realTime = []
// flow_realTime2 = []
// flow_predict = []
//
// function setDate(time, tt, isAdd) {
//     var date = getCurTime(time);//也可以直接透传如'2021-5-8'
//     var d = new Date(date);
//     var t_s = d.getTime(); //转化为时间戳毫秒数
//     var newt = new Date(date); //定义一个新时间
//     if (isAdd) {
//         newt.setTime(t_s + tt * 1000); //设置新时间比旧时间多五秒
//     } else {
//         newt.setTime(t_s - tt * 1000); //设置新时间比旧时间少五秒
//     }
//     newt = new Date(newt)
//     var h = newt.getHours();
//     var m = newt.getMinutes();
//     var s = newt.getSeconds();
//     return zeroPad(h) + ':' + zeroPad(m) + ':' + zeroPad(s);
// }
// function getCurTime(time) {
//     var myDate = new Date();
//     var nowYear = myDate.getFullYear();
//     var nowMonth = myDate.getMonth() + 1;
//     var nowDay = myDate.getDate();
//     return nowYear + '-' + nowMonth + '-' + nowDay + ' ' + time;
// }
// function zeroPad(n) {
//     return n < 10 ? '0' + n : n;
// }
//
// function flow_analysis1() {
//     $.ajax({
//         url: "/flow_analysis/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             console.log(list.length)
//             var XData = [];
//             var date = new Date();
//             var now = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
//             var t_s = date.getTime();
//             var newt = new Date()
//             if (flow_predict.length > 19) {
//                 for (var j = 0; j < 13; j++) {
//                     flow_realTime[j] = flow_realTime[j + 1]
//                 }
//                 flow_realTime[13] = (parseFloat(flow_realTime[14]) + Math.random()).toString()
//                 flow_realTime[14] = flow_predict[15]
//                 flow_realTime[15] = null
//                 flow_predict.shift()
//                 flow_realTime2.shift()
//                 $.each(list, function (i, n) {
//                     if (i == 19) {
//                         flow_predict.push((parseInt(n[0]) + Math.random()).toString())
//                         flow_realTime2.push((parseInt(n[0]) + Math.random()).toString())
//                     }
//                     if (i < 14) {
//                         XData.push(setDate(now, 5 * (14 - i), false));
//                     } else if (i > 14) {
//                         XData.push(setDate(now, 5 * (i - 14), true));
//                     } else {
//                         XData.push(now);
//                     }
//                 });
//             } else {
//                 flow_realTime = []
//                 flow_realTime2 = []
//                 flow_predict = []
//                 $.each(list, function (i, n) {
//                     if (i < Math.floor(list.length * 0.75)) {
//                         flow_realTime.push(n[0])
//                         flow_realTime2.push((parseInt(n[0]) + Math.random()).toString())
//                         flow_predict.push((parseInt(n[0]) + Math.random()).toString())
//                     } else if (i > Math.floor(list.length * 0.75)) {
//                         flow_realTime.push(null)
//                         flow_realTime2.push((parseInt(n[0]) + Math.random()).toString())
//                         flow_predict.push((parseInt(n[0]) + Math.random()).toString())
//                     } else {
//                         flow_realTime.push(n[0])
//                         flow_realTime2.push((parseInt(n[0]) + Math.random()).toString())
//                         flow_predict.push(n[0])
//                     }
//                     if (i < 14) {
//                         XData.push(setDate(now, 5 * (14 - i), false));
//                     } else if (i > 14) {
//                         XData.push(setDate(now, 5 * (i - 14), true));
//                     } else {
//                         XData.push(now);
//                     }
//                 });
//             }
//             dataMainBottom = {
//                 "XData": XData,
//                 "YData1": flow_realTime,
//                 "YData2": flow_predict
//             };
//             option = {
//                 tooltip: {trigger: 'axis', axisPointer: {lineStyle: {color: '#fff'}}},
//                 legend: {
//                     icon: 'rect',
//                     itemWidth: 14, itemHeight: 5, itemGap: 10,
//                     data: ['实时流量', '预测流量'],
//                     right: '10px', top: '0px',
//                     textStyle: {fontSize: 12, color: '#fff'},
//                     show: true
//                 },
//                 grid: {x: 45, y: 35, x2: 30, y2: 90},
//                 xAxis: [{
//                     type: 'category',
//                     boundaryGap: false,
//                     axisLine: {lineStyle: {color: '#57617B'}},
//                     axisLabel: {textStyle: {color: '#fff'}},
//                     textStyle: {fontSize: 3},
//                     data: dataMainBottom.XData
//                 }],
//                 yAxis: [
//                     {
//                         type: 'value',
//                         max : 10,
//                         axisTick: {
//                             show: false
//                         },
//                         axisLine: {lineStyle: {color: '#57617B'}},
//                         axisLabel: {
//                             margin: 10,
//                             textStyle: {fontSize: 12},
//                             textStyle: {color: '#fff'},
//                             formatter: '{value}MB'
//                         },
//                         splitLine: {lineStyle: {color: '#57617B'}}
//                     }, {
//                         type: 'value',
//                         max : 10,
//                         axisTick: {
//                             show: false
//                         },
//                         axisLine: {lineStyle: {color: '#57617B'}},
//                         axisLabel: {
//                             margin: 10,
//                             textStyle: {fontSize: 12},
//                             textStyle: {color: 'rgba(0,0,0,0)'},
//                             formatter: '{value}MB'
//                         },
//                         splitLine: {lineStyle: {color: '#57617B'}}
//                     }, {
//                         type: 'value',
//                         max : 300,
//                         axisTick: {
//                             show: false
//                         },
//                         axisLine: {lineStyle: {color: '#57617B'}},
//                         axisLabel: {
//                             margin: 10,
//                             textStyle: {fontSize: 9},
//                             textStyle: {color: 'rgba(0,0,0,0)'},
//                             formatter: '{value}MB'
//                         },
//                         splitLine: {lineStyle: {color: '#57617B'}}
//                     }
//                 ],
//                 series: [
//                     {
//                         name: '实时流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 0,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(122,234,19,0)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(185,150,248,0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#03C2EC'}},
//                         data: dataMainBottom.YData1
//                     },
//                     {
//                         name: '预测流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2, type: 'dotted'}},
//                         yAxisIndex: 0,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(3, 194, 236, 0)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(3, 194, 236, 0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#d2102d'}},
//                         data: dataMainBottom.YData2
//                     }
//                 ]
//             };
//             var myChart = echarts.init(document.getElementById('mainBottom2'));
//             myChart.setOption(option);
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// }
//
// function flow_analysis() {
//     $.ajax({
//         url: "/flow_analysis/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             var XData = [];
//             var YData1 = [];
//             var YData2 = [];
//             var YData3 = [];
//             var date = new Date();
//             var now = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
//             var t_s = date.getTime();
//             var newt = new Date()
//             $.each(list, function (i, n) {
//                 if (i < 15) {
//                     YData1.push(n[0])
//                     YData2.push(null)
//                 } else if (i > 15) {
//                     YData1.push(null)
//                     YData2.push(n[0])
//                 } else {
//                     YData1.push(n[0])
//                     YData2.push(n[0])
//                 }
//                 if (i < 14) {
//                     XData.push(setDate(now, 5 * (14 - i), false));
//                 } else if (i > 14) {
//                     XData.push(setDate(now, 5 * (i - 14), true));
//                 } else {
//                     XData.push(now);
//                 }
//             });
//             dataMainBottom = {
//                 "XData": XData,
//                 "YData1": YData1,
//                 "YData2": YData2
//             };
//             option = {
//                 tooltip: {trigger: 'axis', axisPointer: {lineStyle: {color: '#fff'}}},
//                 legend: {
//                     icon: 'rect',
//                     itemWidth: 14, itemHeight: 5, itemGap: 10,
//                     data: ['实时流量', '预测流量'],
//                     right: '10px', top: '0px',
//                     textStyle: {fontSize: 12, color: '#fff'},
//                     show: true
//                 },
//                 grid: {x: 45, y: 35, x2: 30, y2: 90},
//                 xAxis: [{
//                     type: 'category',
//                     boundaryGap: false,
//                     axisLine: {lineStyle: {color: '#57617B'}},
//                     axisLabel: {textStyle: {color: '#fff'}},
//                     textStyle: {fontSize: 3},
//                     data: dataMainBottom.XData
//                 }],
//                 yAxis: [
//                     {
//                         type: 'value',
//                         max : 10,
//                         axisTick: {
//                             show: false
//                         },
//                         axisLine: {lineStyle: {color: '#57617B'}},
//                         axisLabel: {
//                             margin: 10,
//                             textStyle: {fontSize: 12},
//                             textStyle: {color: '#fff'},
//                             formatter: '{value}MB'
//                         },
//                         splitLine: {lineStyle: {color: '#57617B'}}
//                     }, {
//                         type: 'value',
//                         max : 10,
//                         axisTick: {
//                             show: false
//                         },
//                         axisLine: {lineStyle: {color: '#57617B'}},
//                         axisLabel: {
//                             margin: 10,
//                             textStyle: {fontSize: 12},
//                             textStyle: {color: 'rgba(0,0,0,0)'},
//                             formatter: '{value}MB'
//                         },
//                         splitLine: {lineStyle: {color: '#57617B'}}
//                     }
//                 ],
//                 series: [
//                     {
//                         name: '实时流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 0,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(122,234,19,0)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(185,150,248,0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#03C2EC'}},
//                         data: dataMainBottom.YData1
//                     },
//                     {
//                         name: '预测流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2, type: 'dotted'}},
//                         yAxisIndex: 0,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(3, 194, 236, 0)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(3, 194, 236, 0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#d2102d'}},
//                         data: dataMainBottom.YData2
//                     }
//                 ]
//             };
//             var myChart = echarts.init(document.getElementById('mainBottom2'));
//             myChart.setOption(option);
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// }
// setInterval(flow_analysis1(), 3000);
// setInterval(flow_analysis1, 3000);
//
// //行为计数
// behavior_count_number = []
// function behavior_count() {
//     $.ajax({
//         url: "/behavior_count/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             var XData = [];
//             var date = new Date();
//             var now = date.getHours().toString() + ':' + date.getMinutes().toString() + ':' + date.getSeconds().toString();
//             var t_s = date.getTime();
//             var newt = new Date()
//             if (behavior_count_number.length > 0) {
//                 behavior_count_number.shift()
//                 $.each(list, function (i, n) {
//                     XData.push(setDate(now, 5 * (list.length - i - 1), false));
//                     if (i == (behavior_count_number.length - 1)) {
//                         behavior_count_number.push(n[0])
//                     }
//                 });
//             } else {
//                 $.each(list, function (i, n) {
//                     XData.push(setDate(now, 5 * (list.length - i - 1), false));
//                     behavior_count_number.push(n[0])
//                 });
//             }
//             var myChart = echarts.init(document.getElementById('echarts_3'));
//             option = {
//                 tooltip : {
//                     trigger: 'axis'
//                 },
//                 legend: {
//                     orient: 'vertical',
//                     data:['简易程序案件数']
//                 },
//                 grid: {
//                     left: '3%',
//                     right: '3%',
//                     top:'8%',
//                     bottom: '5%',
//                     containLabel: true
//                 },
//                 color:['#a4d8cc','#25f3e6'],
//                 toolbox: {
//                     show : false,
//                     feature : {
//                         mark : {show: true},
//                         dataView : {show: true, readOnly: false},
//                         magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
//                         restore : {show: true},
//                         saveAsImage : {show: true}
//                     }
//                 },
//
//                 calculable : true,
//                 xAxis : [
//                     {
//                         type : 'category',
//                         axisTick:{show:false},
//                         boundaryGap : false,
//                         axisLabel: {
//                             textStyle:{
//                                 color: '#ccc',
//                                 fontSize:'12'
//                             },
//                             lineStyle:{
//                                 color:'#2c3459',
//                             },
//                             interval: {default: 0},
//                             rotate:0,
//                             formatter : function(params){
//                                 var newParamsName = "";// 最终拼接成的字符串
//                                 var paramsNameNumber = params.length;// 实际标签的个数
//                                 var provideNumber = 8;// 每行能显示的字的个数
//                                 var rowNumber = Math.ceil(paramsNameNumber / provideNumber);// 换行的话，需要显示几行，向上取整
//                                 /**
//                                  * 判断标签的个数是否大于规定的个数， 如果大于，则进行换行处理 如果不大于，即等于或小于，就返回原标签
//                                  */
//                                 // 条件等同于rowNumber>1
//                                 if (paramsNameNumber > provideNumber) {
//                                     /** 循环每一行,p表示行 */
//                                     var tempStr = "";
//                                     tempStr=params.substring(0,4);
//                                     newParamsName = tempStr+"...";// 最终拼成的字符串
//                                 } else {
//                                     // 将旧标签的值赋给新标签
//                                     newParamsName = params;
//                                 }
//                                 //将最终的字符串返回
//                                 return newParamsName
//                             }
//
//                         },
//                         data: XData
//                     }
//                 ],
//                 yAxis : {
//
//                     type : 'value',
//                     axisLabel: {
//                         textStyle: {
//                             color: '#ccc',
//                             fontSize:'12',
//                         }
//                     },
//                     axisLine: {
//                         lineStyle:{
//                             color:'rgba(160,160,160,0.3)',
//                         }
//                     },
//                     splitLine: {
//                         lineStyle:{
//                             color:'rgba(160,160,160,0.3)',
//                         }
//                     },
//
//                 }
//                 ,
//                 series : [
//                     {
//                         // name:'简易程序案件数',
//                         type:'line',
//                         areaStyle: {
//
//                             normal: {type: 'default',
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 0.8, [{
//                                     offset: 0,
//                                     color: '#25f3e6'
//                                 }, {
//                                     offset: 1,
//                                     color: '#0089ff'
//                                 }], false)
//                             }
//                         },
//                         smooth:true,
//                         itemStyle: {
//                             normal: {areaStyle: {type: 'default'}}
//                         },
//                         data: behavior_count_number
//                     }
//                 ]
//             };
//             myChart.setOption(option);
//             window.addEventListener("resize",function(){
//                 myChart.resize();
//             });
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// }
// setInterval(behavior_count(), 3000);
// setInterval(behavior_count, 3000);
//
// //实时行为概览
// function behavior_overview() {
//     $.ajax({
//         url: "/behavior_overview/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             $('#behavior_overview').empty("");
//             $.each(list, function (i,n){
//                 if (n[3] == '-') {
//                     n[3] = 'undefined';
//                 }
//                 /*
//                 if (n[4] == '其它') {
//                     var r = Math.random();
//                     if (r > 0.8) {
//                         n[4] = '文件传输'
//                     } else if (r > 0.6) {
//                         n[4] = '邮件传输'
//                     } else if (r > 0.4) {
//                         n[4] = '网络通讯'
//                     } else if (r > 0.2) {
//                         n[4] = '网络管理'
//                     } else {
//                         n[4] = '其它'
//                     }
//                 }
//
//                  */
//                 if (n[0] == '182.3.32.3' || n[0] == '52.16.37.10') {
//                     $('#behavior_overview').append($("<tr><td class=\"a1\" style='width: 24%; color: red'>"+n[0]+"</td><td class=\"a1\" style='width: 24%; color:red'>"+n[1]+"</td><td class=\"a1\" style='width: 13.2%; color:red'>"+n[2]+
//                     "</td><td class=\"a1\" style='width: 13.7%; color:red'>"+n[3]+"</td><td class=\"a1\" style='width: 13.7%; color:red'>"+n[4]+"</td><td class=\"a1\" style='width: 10.7%'><a href='http://10.0.21.51:8888/#/'><font color='red'>详情</font></a></td></tr>"));
//                 } else {
//                     $('#behavior_overview').append($("<tr><td class=\"a1\" style='width: 24%'>"+n[0]+"</td><td class=\"a1\" style='width: 24%'>"+n[1]+"</td><td class=\"a1\" style='width: 13.2%'>"+n[2]+
//                     "</td><td class=\"a1\" style='width: 13.7%'>"+n[3]+"</td><td class=\"a1\" style='width: 13.7%'>"+n[4]+"</td><td class=\"a1\" style='width: 10.7%'><a href='http://10.0.21.51:8888/#/'><font color='white'>详情</font></a></td></tr>"));
//                 }
//
//             });
//             // $(function () {
//             //     $('.scrollDiv').liMarquee({
//             //         direction: 'down',//向上滚动
//             //         runshort: false,//内容不足时不滚动
//             //         scrollamount: 20,//速度
//             //     });
//             // });
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             // 状态码
//             console.log(XMLHttpRequest.status);
//             // 状态
//             console.log(XMLHttpRequest.readyState);
//             // 错误信息
//             console.log(textStatus);
//         }
//     })
// };
// //behavior_overview();
// setInterval(behavior_overview(), 3000);
// setInterval(behavior_overview, 3000);
//
//
// //流量读入
// function readPcapx() {
//     $.ajax({
//         url: "/readCsv/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//
//         }
//     })
// }
// setInterval(readPcapx(), 3000);
// setInterval(readPcapx, 3000);
//
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
//
//
// function mock_data() {
//      $.ajax({
//          url: "/mock_data/", //别忘了加双引号
//          type: "GET",
//          success: function (list) {
//
//         }
//     })
// }
// setInterval(mock_data(), 3000);
// setInterval(mock_data, 3000);
//
//
//
