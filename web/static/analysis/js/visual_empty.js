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
                YData1.push(0)
                YData2.push(0)
                YData3.push(0)
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
                    itemWidth: 14, itemHeight: 5, itemGap: 10,
                    data: ['总流量', '入境流量', '出境流量'],
                    right: '10px', top: '0px',
                    textStyle: {fontSize: 12, color: '#fff'},
                    show:false
                },
                grid: {x: 45, y: 35, x2: 30, y2: 90},
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,
                    axisLine: {lineStyle: {color: '#57617B'}},
                    axisLabel: {textStyle: {color: '#fff'}},
                    data: dataMainBottom.XData,
                    show:false
                }],
                yAxis: [
                    {
                        type: 'value',
                        axisTick: {
                            show: false
                        },
                        axisLine: {lineStyle: {color: '#57617B'}},
                        axisLabel: {
                            margin: 10,
                            textStyle: {fontSize: 12},
                            textStyle: {color: '#fff'},
                            formatter: '{value}MB'
                        },
                        splitLine: {lineStyle: {color: '#57617B'}}
                    }, {
                        type: 'value',
                        axisTick: {
                            show: false
                        },
                        axisLine: {lineStyle: {color: '#57617B'}},
                        axisLabel: {
                            margin: 10,
                            textStyle: {fontSize: 12},
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
                        name: '入境流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
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
                        name: '出境流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
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
setInterval(mainBottomx, 2000);

//清除数据
function clear_analysis() {
    $.ajax({
        url: "/clear_analysis/", //别忘了加双引号
        type: "GET",
        success: function (list) {

        }
    })
}

clear_analysis()


