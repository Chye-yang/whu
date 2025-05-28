// //传输层分析
// function table5x() {
//     $.ajax({
//         url: "/table5/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             $('#table5').empty("");
//             $.each(list, function (i,n){
//                 console.log(n);
//                 $('#table5').append($("<tr><td>"+n[6]+"</td><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+ n[2]+
//                     "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+"</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table5x(), 2000);
// setInterval(table5x, 2000);
//
// //网络层分析
// function table6x() {
//     $.ajax({
//         url: "/table6/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             $('#table6').empty("");
//             $.each(list, function (i,n){
//                 $('#table6').append($("<tr><td>"+n[6]+"</td><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+ n[2]+
//                     "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+"</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table6x(), 2000);
// setInterval(table6x, 2000);
//
// //mainTop
// function mainTopx() {
//     $.ajax({
//         url: "/mainTop/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             document.getElementById("mainTop1").innerText = list[0]
//             document.getElementById("mainTop2").innerText = list[1]
//             document.getElementById("mainTop3").innerText = list[2]
//             document.getElementById("mainTop4").innerText = list[3]
//         }
//     })
// }
// setInterval(mainTopx(), 2000);
// setInterval(mainTopx, 2000);
//
// //实时流量分析
// function mainBottomx() {
//     $.ajax({
//         url: "/mainBottom/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             var XData = [];
//             var YData1 = [];
//             var YData2 = [];
//             var YData3 = [];
//             $.each(list, function (i, n) {
//                 XData.push(n[0])
//                 YData1.push(n[1])
//                 YData2.push(n[2])
//                 YData3.push(n[3])
//             });
//             dataMainBottom = {
//                 "XData": XData,
//                 "YData1": YData1,
//                 "YData2": YData2,
//                 "YData3": YData3,
//             };
//             option = {
//                 tooltip: {trigger: 'axis', axisPointer: {lineStyle: {color: '#fff'}}},
//                 legend: {
//                     icon: 'rect',
//                     itemWidth: 14, itemHeight: 5, itemGap: 10,
//                     data: ['总流量', '入境流量', '出境流量'],
//                     right: '10px', top: '0px',
//                     textStyle: {fontSize: 12, color: '#fff'}
//                 },
//                 grid: {x: 45, y: 35, x2: 30, y2: 90},
//                 xAxis: [{
//                     type: 'category',
//                     boundaryGap: false,
//                     axisLine: {lineStyle: {color: '#57617B'}},
//                     axisLabel: {textStyle: {color: '#fff'}},
//                     data: dataMainBottom.XData
//                 }],
//                 yAxis: [
//                     {
//                         type: 'value',
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
//                         name: '总流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 0,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(122,234,19,0.3)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(185,150,248,0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#c40d44'}},
//                         data: dataMainBottom.YData1
//                     },
//                     {
//                         name: '入境流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 1,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(3, 194, 236, 0.3)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(3, 194, 236, 0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#03C2EC'}},
//                         data: dataMainBottom.YData2
//                     },
//                     {
//                         name: '出境流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 1,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(218, 57, 20, 0.3)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(218, 57, 20, 0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#DA3914'}},
//                         data: dataMainBottom.YData3
//                     }
//                 ]
//             };
//             var myChart = echarts.init(document.getElementById('mainBottom'));
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
// setInterval(mainBottomx(), 2000);
// setInterval(mainBottomx, 2000);
//
// //链路层分析
// function table7x() {
//     $.ajax({
//         url: "/table7/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             $('#table7').empty("");
//             $.each(list, function (i,n){
//                 $('#table7').append($("<tr><td>"+n[6]+"</td><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+ n[2]+
//                     "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+"</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table7x(), 2000);
// setInterval(table7x, 2000);
//
// //端口分析
// function table8x() {
//     $.ajax({
//         url: "/table8/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             $('#table8').empty("");
//             $.each(list, function (i,n){
//                 $('#table8').append($("<tr><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+n[2]+
//                     "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+
//                     "</td><td>"+n[6]+"</td><td>"+n[7]+"</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table8x(), 2000);
// setInterval(table8x, 2000);
//
// //流量读入
// function readPcapx() {
//     $.ajax({
//         url: "/readPcap/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//
//         }
//     })
// }
// setInterval(readPcapx(), 2000);
// setInterval(readPcapx, 2000);
//
//
