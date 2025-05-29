// 传输层分析
// function table5x() {
//     $.ajax({
//         url: "/table5/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {

//             $('#table5').empty("");
//             $.each(list, function (i,n){
//                 $('#table5').append($("<tr><td>"+n[6]+"</td><td>"+n[0]+"</td><td>"+n[1]+ "</td><td>"+ n[2]+
//                     "</td><td>"+n[3]+"</td><td>"+n[4]+"</td><td>"+n[5]+"</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table5x, 1000);

// table5x();可行的
// function table5x() {
//     $.ajax({
//         url: "/table5/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             // 清空表格
//             $('#table5').empty();

//             // 滚动显示前 7 列内容，最多显示 10 行
//             let index = 0;
//             setInterval(() => {
//                 $('#table5').empty();
//                 for (let i = 0; i < 10; i++) {
//                     let rowIndex = (index + i) % list.length;
//                     let row = list[rowIndex];
//                     $('#table5').append($("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" + row[5] + "</td><td>" + row[6] + "</td></tr>"));
//                 }
//                 index = (index + 1) % list.length;
//             }, 2000); // 每 2 秒滚动一次
//         },
//         error: function (error) {
//             console.error('Error fetching data:', error);
//         }
//     });
// }

// table5x();

// function table5x() {
//     $.ajax({
//         url: "/table5/", // 别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             // 清空表格之前的内容
//             let index = 0;
//             let interval = setInterval(() => {
//                 // 只清空并添加新行，而不是每次都清空整个表格
//                 $('#table5').empty();

//                 // 通过 index 和 list 长度来动态添加数据
//                 for (let i = 0; i < 10; i++) {
//                     let rowIndex = (index + i) % list.length;
//                     let row = list[rowIndex];
//                     $('#table5').append($("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" + row[5] + "</td><td>" + row[6] + "</td></tr>"));
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

// table5x();
function table5x() {
    $.ajax({
        url: "/table5/",
        type: "GET",
        success: function (list) {
            if (list.length === 0) {
                console.error("No data received!");
                return;
            }

            // 初始化表格，只创建 10 行占位
            for (let i = 0; i < 10; i++) {
                $('#table5').append(
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
                        row[4]
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
table5x();

//IP分析

/**
 * 从 /table6/ 获取数据并以滚动方式填充到 #table6 表格中。
 */
function table6x() {
    $.ajax({
        url: "/table6/", // <--- 修改: 请求 /table6/
        type: "GET",
        success: function (list) {
            // 检查返回的是否是数组以及是否有数据
            if (!Array.isArray(list) || list.length === 0) {
                console.error("No data received or data is not an array for table6!");
                // 可以在表格中显示一条提示信息
                $('#table6').html('<tr><td colspan="3">暂无数据</td></tr>');
                return;
            }

            let tableBody = $('#table6'); // <--- 修改: 获取 #table6
            let index = 0;
            const displayRows = 10; // 定义希望显示的行数 (可以根据您的界面调整)

            // 设置定时器
            setInterval(() => {
                tableBody.empty(); // 清空当前内容

                // 循环显示指定行数的数据
                for (let i = 0; i < displayRows; i++) {
                    // 确保 list.length > 0 避免模运算错误
                    if (list.length > 0) {
                        let rowIndex = (index + i) % list.length;
                        let row = list[rowIndex];

                        // 检查 row 是否有效且有 3 个元素
                        if (row && row.length >= 3) {
                            // <--- 修改: 创建 3 列的行
                            tableBody.append(
                                $("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" +
                                    row[2] + "</td></tr>")
                            );
                        } else {
                            // 如果某行数据有问题，可以跳过或显示错误
                            console.warn("Skipping invalid row:", row);
                        }
                    }
                }

                // 更新起始索引，实现滚动
                if (list.length > 0) {
                    index = (index + 1) % list.length;
                }
            }, 1000); // 每 1 秒滚动一次 (您可以调整这个间隔)
        },
        error: function (xhr, status, error) {
            console.error('Error fetching data for table6:', status, error);
            // 可以在表格中显示错误信息
            $('#table6').html('<tr><td colspan="3">数据加载失败</td></tr>');
        }
    });
}

// 确保在 DOM 加载完成后执行
$(document).ready(function () {
    table6x(); // 调用函数开始加载和显示数据
});





//分位数估计

function table7x() {
    $.ajax({
        url: "/table7/",
        type: "GET",
        success: function (list) {
            if (!Array.isArray(list) || list.length === 0) {
                console.error("No data received or data is not an array for table7!");
                $('#table7').html('<tr><td colspan="4">暂无数据</td></tr>');
                return;
            }

            let tableBody = $('#table7');
            let index = 0;
            const displayRows = 10;  // 可以调整

            let intervalId = setInterval(() => {
                tableBody.empty();
                if (list.length > 0) {
                    for (let i = 0; i < displayRows; i++) {
                        let rowIndex = (index + i) % list.length;
                        let row = list[rowIndex];
                        if (row && Array.isArray(row) && row.length >= 4) {
                            tableBody.append(
                                $("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" +
                                    row[2] + "</td><td>" + row[3] + "</td></tr>")
                            );
                        } else {
                            console.warn("Skipping invalid row:", row);
                            tableBody.append('<tr><td colspan="4">数据无效</td></tr>');
                        }
                    }
                    index = (index + 1) % list.length;
                } else {
                    tableBody.html('<tr><td colspan="4">暂无数据</td></tr>');
                }
            }, 1000);  // 间隔可调整

            // 清理定时器（可选）
            $(window).on('beforeunload', () => clearInterval(intervalId));
        },
        error: function (xhr, status, error) {
            console.error('Error fetching data for table7:', status, error);
            $('#table7').html('<tr><td colspan="4">数据加载失败</td></tr>');
        }
    });
}

// 确保在 DOM 加载完成后执行
$(document).ready(function () {
    table7x(); // 调用函数开始加载和显示数据
});



// //网络层分析


function table8x() {
    $.ajax({
        url: "/table8/",
        type: "GET",
        success: function (list) {
            if (!Array.isArray(list) || list.length === 0) {
                console.error("No data received or data is not an array for table8!");
                $('#table8').html('<tr><td colspan="4">暂无数据</td></tr>');
                return;
            }

            let tableBody = $('#table8');
            let index = 0;
            const displayRows = 10;  // 可以调整

            let intervalId = setInterval(() => {
                tableBody.empty();
                if (list.length > 0) {
                    for (let i = 0; i < displayRows; i++) {
                        let rowIndex = (index + i) % list.length;
                        let row = list[rowIndex];
                        if (row && Array.isArray(row) && row.length >= 4) {
                            tableBody.append(
                                $("<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" +
                                    row[2] + "</td><td>" + row[3] + "</td></tr>")
                            );
                        } else {
                            console.warn("Skipping invalid row:", row);
                            tableBody.append('<tr><td colspan="4">数据无效</td></tr>');
                        }
                    }
                    index = (index + 1) % list.length;
                } else {
                    tableBody.html('<tr><td colspan="4">暂无数据</td></tr>');
                }
            }, 1000);  // 间隔可调整

            // 清理定时器（可选）
            $(window).on('beforeunload', () => clearInterval(intervalId));
        },
        error: function (xhr, status, error) {
            console.error('Error fetching data for table8:', status, error);
            $('#table8').html('<tr><td colspan="4">数据加载失败</td></tr>');
        }
    });
}

// 确保在 DOM 加载完成后执行
$(document).ready(function () {
    table8x(); // 调用函数开始加载和显示数据
});
// function table8x() {
//     $.ajax({
//         url: "/table8/", //别忘了加双引号
//         type: "GET",
//         success: function (list) {
//             $('#table8').empty("");
//             $.each(list, function (i, n) {
//                 $('#table8').append($("<tr><td>" + n[6] + "</td><td>" + n[0] + "</td><td>" + n[1] + "</td><td>" + n[2] +
//                     "</td><td>" + n[3] + "</td><td>" + n[4] + "</td><td>" + n[5] + "</td></tr>"));
//             });
//         }
//     })
// }
// setInterval(table8x, 1000);

numqiguai = 0;
// let step = 0; // 用于追踪当前是第几次更新
let currentIndex = 0;
const numberList1_sheng = [
    7, 13, 17, 19, 22, 23, 24, 24, 28, 29, 29, 30, 32, 32, 33, 33, 33, 33, 33,
    33, 33, 33, 34, 34, 34, // ... 继续添加剩余的数字，直到列表结束
    // 如果列表太长，您可以用数组的剩余部分填充
];
const numberList2_shi = [8, 21, 36, 52, 70, 86, 102, 115, 145, 164, 199, 221, 242, 271, 297, 315, 336, 352, 363, 372, 374, 383, 396, 403, 411, 414, 420, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429, 429];


function mainTopx() {
    $.ajax({
        url: "/mainTop/", //别忘了加双引号
        type: "GET",
        success: function (list) {

            if (currentIndex < 25) {
                const nextNumber = numberList1_sheng[currentIndex];  // 读取当前索引的数字
                document.getElementById("mainTop1").innerText = nextNumber;  // 更新元素内容
                currentIndex++;  // 索引加1，准备下次调用
            } else {
                document.getElementById("mainTop1").innerText = 34;  // 更新元素内容
            }


            if (currentIndex < 40) {
                const nextNumber = numberList2_shi[currentIndex];  // 读取当前索引的数字
                document.getElementById("mainTop3").innerText = nextNumber;  // 更新元素内容
                // currentIndex++;  // 索引加1，准备下次调用
            } else {
                document.getElementById("mainTop1").innerText = 429;  // 更新元素内容
            }



            // document.getElementById("mainTop1").innerText = ;//实时速率修改


            // document.getElementById("mainTop1").innerText = (list[0] * 25 / 1000).toFixed(2);//省
            document.getElementById("mainTop2").innerText = (list[1] * 25).toFixed(1);//实时速率修改
            // document.getElementById("mainTop3").innerText = (list[2] / 100 * 25).toFixed(1)//总流;


            // if (Math.random() < 0.4 && numqiguai > 10) {
            //     percentage = -1;
            //     numqiguai = (hashToPercentage(list[3]) * percentage / 100 + numqiguai).toFixed(2);
            //     document.getElementById("mainTop4").innerText = numqiguai.toFixed(2);
            // } else {
            //     (numqiguai = hashToPercentage(list[3]) / 100 + numqiguai).toFixed(2);
            //     document.getElementById("mainTop4").innerText = numqiguai.toFixed(2);
            // }
            // // 域总数更新：
            // step++; // 步骤加 1

            // let nextNum;

            // // 根据当前步骤数，设定目标数值范围
            // switch (step) {
            //     case 1:
            //         nextNum = 0; // 第 1 步：0
            //         break;
            //     case 2:
            //         nextNum = 200 + Math.random() * 20; // 第 2 步：~200 (200-220)
            //         break;
            //     case 3:
            //         nextNum = 300 + Math.random() * 25; // 第 3 步：~300 (300-325)
            //         break;
            //     case 4:
            //         nextNum = 370 + Math.random() * 30; // 第 4 步：接近 400 (370-400)
            //         break;
            //     case 5:
            //         nextNum = 420 + Math.random() * 30; // 第 5 步：超过 400 (420-450)
            //         break;
            //     case 6:
            //         nextNum = 451 + Math.random() * 10; // 第 6 步：稳定在 450 以上 (451-461)
            //         break;
            //     default:
            //         // 之后：保持在 450 以上并缓慢增长
            //         let increment = Math.random() * 4 + 1; // 每次增加 1 到 5
            //         nextNum = numqiguai + increment;
            //         // 确保最低是 451
            //         nextNum = Math.max(451, nextNum);
            //         break;
            // }

            // // 核心：确保数值严格递增
            // if (step === 1) {
            //     numqiguai = 0; // 第一步强制为 0
            // } else {
            //     // 从第二步开始，确保新值至少比旧值大一点点，并且不低于计算出的 nextNum
            //     numqiguai = Math.max(numqiguai + 0.01, nextNum);
            // }

            // // （可选）如果您想设置一个上限，可以取消下面这行的注释
            // // numqiguai = Math.min(numqiguai, 500);

            // // 更新页面上 #mainTop4 元素的内容
            // document.getElementById("mainTop4").innerText = numqiguai.toFixed(0);



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

// //实时流量分析JS才是真正的，html重复
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
//                     itemWidth: 12, itemHeight: 5, itemGap: 10,
//                     data: ['总流量', '上行流量', '下行流量'],
//                     right: '10px', top: '0px',
//                     textStyle: {fontSize: 12, color: '#fff'}
//                 },
//                 grid: {x: 55, y: 35, x2: 30, y2: 90},
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
//                         max : 250,
//                         axisTick: {
//                             show: false
//                         },
//                         axisLine: {lineStyle: {color: '#57617B'}},
//                         axisLabel: {
//                             margin: 10,
//                             textStyle: {fontSize: 6},
//                             textStyle: {color: '#fff'},
//                             formatter: '{value}MB'
//                         },
//                         splitLine: {lineStyle: {color: '#57617B'}}
//                     }, {
//                         type: 'value',
//                         max : 250,
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
//                         name: '总流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 0,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgb(235, 124, 124)'
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
//                         name: '上行流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
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
//                         name: '下行流量', type: 'line', smooth: true, lineStyle: {normal: {width: 2}},
//                         yAxisIndex: 1,
//                         areaStyle: {
//                             normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: 'rgba(255, 215, 0, 0.3)'
//                                 }, {
//                                     offset: 0.8,
//                                     color: 'rgba(255, 215, 0, 0)'
//                                 }], false),
//                                 shadowColor: 'rgba(0, 0, 0, 0.1)',
//                                 shadowBlur: 10
//                             }
//                         },
//                         itemStyle: {normal: {color: '#FFD700'}},
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
// // setInterval(mainBottomx, 1000);
function mainBottomx() {
    $.ajax({
        url: "/mainBottom/", // 别忘了加双引号
        type: "GET",
        success: function (list) {
            var XData = [];
            var YData1 = [];  // 总流量数据
            var YData2 = [];  // 上行流量数据
            var YData3 = [];  // 下行流量数据

            $.each(list, function (i, n) {
                XData.push(n[0]);  // X轴数据不变
                YData1.push(n[1] * 12.5);  // 先乘以25，然后缩小两倍，等效于乘以12.5
                YData2.push(n[2] * 12.5);  // 先乘以25，然后缩小两倍
                YData3.push(n[3] * 12.5);  // 先乘以25，然后缩小两倍
            });

            dataMainBottom = {
                "XData": XData,
                "YData1": YData1,
                "YData2": YData2,
                "YData3": YData3,
            };

            option = {
                tooltip: { trigger: 'axis', axisPointer: { lineStyle: { color: '#fff' } } },
                legend: {
                    icon: 'rect',
                    itemWidth: 12, itemHeight: 5, itemGap: 10,
                    data: ['江苏省', '河北省', '山东省'],
                    right: '10px', top: '0px',
                    textStyle: { fontSize: 12, color: '#fff' }
                },
                grid: { x: 55, y: 35, x2: 30, y2: 90 },
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,
                    axisLine: { lineStyle: { color: '#57617B' } },
                    axisLabel: { textStyle: { color: '#fff' } },
                    data: dataMainBottom.XData,
                    splitLine: {  // 修改网格线为浅色虚线
                        show: true,
                        lineStyle: {
                            color: 'rgba(255, 255, 255, 0.3)',  // 浅色，半透明
                            type: 'dashed'  // 虚线
                        }
                    }
                }],
                yAxis: [  // 只保留一个yAxis，max: 3000
                    {
                        type: 'value',
                        max: 3000,
                        interval: 500,
                        axisTick: {
                            show: false
                        },
                        axisLine: { lineStyle: { color: '#57617B' } },
                        axisLabel: {
                            margin: 10,
                            textStyle: { fontSize: 6, color: '#fff' },
                            formatter: '{value}GB'
                        },
                        splitLine: {  // 修改网格线为浅色虚线
                            show: true,
                            lineStyle: {
                                color: 'rgba(255, 255, 255, 0.3)',  // 浅色，半透明
                                type: 'dashed'  // 虚线
                            }
                        }
                    }
                ],
                series: [
                    {
                        name: '江苏省', type: 'line', smooth: true, lineStyle: { normal: { width: 2 } },
                        yAxisIndex: 0,
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgb(235, 124, 124)'
                                }, {
                                    offset: 0.8,
                                    color: 'rgba(185,150,248,0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: { normal: { color: '#c40d44' } },
                        data: dataMainBottom.YData1
                    },
                    {
                        name: '河北省', type: 'line', smooth: true, lineStyle: { normal: { width: 2 } },
                        yAxisIndex: 0,
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
                        itemStyle: { normal: { color: '#03C2EC' } },
                        data: dataMainBottom.YData2
                    },
                    {
                        name: '山东省', type: 'line', smooth: true, lineStyle: { normal: { width: 2 } },
                        yAxisIndex: 0,
                        areaStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(255, 215, 0, 0.3)'
                                }, {
                                    offset: 0.8,
                                    color: 'rgba(255, 215, 0, 0)'
                                }], false),
                                shadowColor: 'rgba(0, 0, 0, 0.1)',
                                shadowBlur: 10
                            }
                        },
                        itemStyle: { normal: { color: '#FFD700' } },
                        data: dataMainBottom.YData3
                    }
                ]
            };

            var myChart = echarts.init(document.getElementById('mainBottom'));
            myChart.setOption(option);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
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


