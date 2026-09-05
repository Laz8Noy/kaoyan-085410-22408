// Generated chart code (enhanced)
(function(){
  var style=getComputedStyle(document.documentElement);
  var accent=style.getPropertyValue('--accent').trim();
  var accent2=style.getPropertyValue('--accent2').trim();
  var ink=style.getPropertyValue('--ink').trim();
  var muted=style.getPropertyValue('--muted').trim();
  var rule=style.getPropertyValue('--rule').trim();

  var gradColors=["#dc2626", "#dc2626", "#dc2626", "#dc2626", "#dc2626", "#dc2626", "#dc2626", "#dc2626", "#2563eb", "#2563eb", "#2563eb", "#2563eb", "#2563eb", "#2563eb", "#059669", "#059669", "#059669", "#059669"];

  // Chart 1: Line - 复试线趋势(含2026)
  var c1=echarts.init(document.getElementById('chart-line'),null,{renderer:'svg'});
  var lineData={"years": [2023, 2024, 2025, 2026], "schools": [{"name": "浙江理工大学", "data": [null, null, null, 335]}, {"name": "南京航空航天大学", "data": [330, 335, 340, null]}, {"name": "中山大学", "data": [335, 340, 345, null]}, {"name": "华东理工大学", "data": [325, 330, 338, null]}, {"name": "上海大学", "data": [310, 315, 318, 305]}, {"name": "苏州大学", "data": [328, 333, 337, null]}, {"name": "南京邮电大学", "data": [330, 335, 335, null]}, {"name": "合肥工业大学", "data": [325, 330, 332, null]}, {"name": "深圳大学", "data": [315, 322, 329, 335]}, {"name": "广东工业大学", "data": [300, 305, 308, 301]}, {"name": "广州大学", "data": [280, 296, null, 310]}, {"name": "杭州电子科技大学", "data": [300, 310, 315, 264]}, {"name": "南京信息工程大学", "data": [300, 305, 310, null]}, {"name": "安徽大学", "data": [290, 295, 300, null]}, {"name": "华南农业大学", "data": [null, null, null, 294]}, {"name": "江苏大学", "data": [280, 285, 285, 264]}, {"name": "上海理工大学", "data": [280, 285, 288, null]}, {"name": "浙江工业大学", "data": [290, 295, 295, null]}]};
  c1.setOption({
    animation:false,
    tooltip:{trigger:'axis',appendToBody:true},
    legend:{data:lineData.schools.map(function(s){return s.name}),top:0,type:'scroll',fontSize:10},
    grid:{top:60,left:50,right:20,bottom:30},
    xAxis:{type:'category',data:lineData.years,axisLine:{lineStyle:{color:rule}}},
    yAxis:{type:'value',name:'复试线',min:250,max:360,axisLine:{lineStyle:{color:rule}},splitLine:{lineStyle:{color:rule}}},
    series:lineData.schools.map(function(s,i){
      return {name:s.name,type:'line',data:s.data,smooth:true,
        connectNulls:true,
        lineStyle:{width:2},itemStyle:{color:gradColors[i]},
        emphasis:{focus:'series'}};
    })
  });
  window.addEventListener('resize',function(){c1.resize()});

  // Chart 2: Bar - 2026复试线 vs 平均分
  var c2=echarts.init(document.getElementById('chart-bar'),null,{renderer:'svg'});
  var barData={"schools": ["浙江理工大学", "南京航空航天大学", "中山大学", "华东理工大学", "上海大学", "苏州大学", "南京邮电大学", "合肥工业大学", "深圳大学", "广东工业大学", "广州大学", "杭州电子科技大学", "南京信息工程大学", "安徽大学", "华南农业大学", "江苏大学", "上海理工大学", "浙江工业大学"], "lines": [335, 340, 345, 338, 305, 337, 335, 332, 335, 301, 310, 264, 310, 300, 294, 264, 288, 295], "avgs": [0, 361, 365, 358, 0, 359, 355, 348, 0, 0, 0, 0, 335, 325, 326, 0, 315, 320]};
  c2.setOption({
    animation:false,
    tooltip:{trigger:'axis',appendToBody:true},
    legend:{data:['2026复试线','2026平均分'],top:0},
    grid:{top:40,left:50,right:20,bottom:90},
    xAxis:{type:'category',data:barData.schools,axisLabel:{rotate:45,fontSize:10,color:ink,interval:0},axisLine:{lineStyle:{color:rule}}},
    yAxis:{type:'value',name:'分数',min:250,max:400,axisLine:{lineStyle:{color:rule}},splitLine:{lineStyle:{color:rule}}},
    series:[
      {name:'2026复试线',type:'bar',data:barData.lines,itemStyle:{color:accent},barGap:'10%'},
      {name:'2026平均分',type:'bar',data:barData.avgs,itemStyle:{color:accent2}}
    ]
  });
  window.addEventListener('resize',function(){c2.resize()});

  // Chart 3: Heat ranking
  var c3=echarts.init(document.getElementById('chart-heat'),null,{renderer:'svg'});
  var heatData={"schools": ["浙江理工大学", "深圳大学", "广东工业大学", "广州大学", "杭州电子科技大学", "华南农业大学", "江苏大学"], "values": [61, 65, 57, 50, 40, 47, 33]};
  c3.setOption({
    animation:false,
    tooltip:{trigger:'axis',appendToBody:true,formatter:function(p){return p[0].name+': 热度'+p[0].value}},
    grid:{top:20,left:120,right:40,bottom:30},
    xAxis:{type:'value',name:'综合热度',max:100,axisLine:{lineStyle:{color:rule}},splitLine:{lineStyle:{color:rule}}},
    yAxis:{type:'category',data:heatData.schools,axisLabel:{fontSize:10,color:ink},axisLine:{lineStyle:{color:rule}}},
    series:[{type:'bar',data:heatData.values,
      itemStyle:{color:function(p){
        var colors=['#dc2626','#dc2626','#dc2626','#dc2626','#2563eb','#2563eb','#2563eb','#2563eb','#2563eb','#2563eb','#059669','#059669','#059669','#059669'];
        return colors[p.dataIndex]||'#6b7280';
      }},
      label:{show:true,position:'right',formatter:'{c}',fontSize:10,color:ink}}]
  });
  window.addEventListener('resize',function(){c3.resize()});
})();