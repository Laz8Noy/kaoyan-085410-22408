// Generated chart code
(function(){
  var style=getComputedStyle(document.documentElement);
  var accent=style.getPropertyValue('--accent').trim();
  var accent2=style.getPropertyValue('--accent2').trim();
  var ink=style.getPropertyValue('--ink').trim();
  var muted=style.getPropertyValue('--muted').trim();
  var rule=style.getPropertyValue('--rule').trim();
  var bg2=style.getPropertyValue('--bg2').trim();
  var cSprint=style.getPropertyValue('--c-sprint').trim();
  var cStable=style.getPropertyValue('--c-stable').trim();
  var cSafety=style.getPropertyValue('--c-safety').trim();

  var schools=["南京航空航天大学", "华东理工大学", "苏州大学", "南京邮电大学", "杭州电子科技大学", "合肥工业大学", "深圳大学", "江苏大学", "浙江工业大学", "安徽大学"];
  var gradColors=["#dc2626","#dc2626","#dc2626","#2563eb","#2563eb","#2563eb","#2563eb","#059669","#059669","#059669"];

  // Chart 1: Line - 复试线趋势
  var c1=echarts.init(document.getElementById('chart-line'),null,{renderer:'svg'});
  var lineData={"years": [2023, 2024, 2025], "schools": [{"name": "南京航空航天大学", "data": [330, 335, 340]}, {"name": "华东理工大学", "data": [325, 330, 338]}, {"name": "苏州大学", "data": [328, 333, 337]}, {"name": "南京邮电大学", "data": [315, 323, 330]}, {"name": "杭州电子科技大学", "data": [310, 320, 327]}, {"name": "合肥工业大学", "data": [313, 321, 328]}, {"name": "深圳大学", "data": [315, 322, 329]}, {"name": "江苏大学", "data": [273, 273, 273]}, {"name": "浙江工业大学", "data": [273, 285, 295]}, {"name": "安徽大学", "data": [280, 290, 298]}]};
  c1.setOption({
    animation:false,
    tooltip:{trigger:'axis',appendToBody:true},
    legend:{data:lineData.schools.map(function(s){return s.name}),top:0,type:'scroll'},
    grid:{top:50,left:50,right:20,bottom:30},
    xAxis:{type:'category',data:lineData.years,axisLine:{lineStyle:{color:rule}}},
    yAxis:{type:'value',name:'复试线',min:250,max:360,axisLine:{lineStyle:{color:rule}},splitLine:{lineStyle:{color:rule}}},
    series:lineData.schools.map(function(s,i){
      return {name:s.name,type:'line',data:s.data,smooth:true,
        lineStyle:{width:2},itemStyle:{color:gradColors[i]},
        emphasis:{focus:'series'}};
    })
  });
  window.addEventListener('resize',function(){c1.resize()});

  // Chart 2: Bar - 复试线 vs 平均分
  var c2=echarts.init(document.getElementById('chart-bar'),null,{renderer:'svg'});
  var barData={"schools": ["南京航空航天大学", "华东理工大学", "苏州大学", "南京邮电大学", "杭州电子科技大学", "合肥工业大学", "深圳大学", "江苏大学", "浙江工业大学", "安徽大学"], "lines": [340, 338, 337, 330, 327, 328, 329, 273, 295, 298], "avgs": [361, 358, 359, 347, 344, 345, 346, 327, 331, 330]};
  c2.setOption({
    animation:false,
    tooltip:{trigger:'axis',appendToBody:true},
    legend:{data:['2025复试线','2025平均分'],top:0},
    grid:{top:40,left:50,right:20,bottom:60},
    xAxis:{type:'category',data:barData.schools,axisLabel:{rotate:35,fontSize:11,color:ink},axisLine:{lineStyle:{color:rule}}},
    yAxis:{type:'value',name:'分数',min:250,max:400,axisLine:{lineStyle:{color:rule}},splitLine:{lineStyle:{color:rule}}},
    series:[
      {name:'2025复试线',type:'bar',data:barData.lines,itemStyle:{color:accent},barGap:'10%'},
      {name:'2025平均分',type:'bar',data:barData.avgs,itemStyle:{color:accent2}}
    ]
  });
  window.addEventListener('resize',function(){c2.resize()});

  // Chart 3: Salary
  var c3=echarts.init(document.getElementById('chart-salary'),null,{renderer:'svg'});
  var salData={"schools": ["南京航空航天大学", "华东理工大学", "苏州大学", "南京邮电大学", "杭州电子科技大学", "合肥工业大学", "深圳大学", "江苏大学", "浙江工业大学", "安徽大学"], "values": [28.6, 26.8, 27.5, 24.2, 23.8, 22.7, 27.2, 18.5, 20.3, 19.7]};
  c3.setOption({
    animation:false,
    tooltip:{trigger:'axis',appendToBody:true,formatter:function(p){return p[0].name+': '+p[0].value+'万/年'}},
    grid:{top:20,left:100,right:30,bottom:30},
    xAxis:{type:'value',name:'万/年',axisLine:{lineStyle:{color:rule}},splitLine:{lineStyle:{color:rule}}},
    yAxis:{type:'category',data:salData.schools,axisLabel:{fontSize:11,color:ink},axisLine:{lineStyle:{color:rule}}},
    series:[{type:'bar',data:salData.values,
      itemStyle:{color:function(p){return gradColors[p.dataIndex]}},
      label:{show:true,position:'right',formatter:'{c}万',fontSize:11,color:ink}}]
  });
  window.addEventListener('resize',function(){c3.resize()});
})();