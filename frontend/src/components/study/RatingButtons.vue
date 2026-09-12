<template>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; width:100%; max-width:500px; position:relative; z-index:1">
    <button @click="$emit('rate', 0)"
            style="border:none; padding:18px 16px; border-radius:16px; font-size:14px; font-weight:800; cursor:pointer; transition:all 0.15s; display:flex; flex-direction:column; align-items:center; gap:4px; text-transform:uppercase; letter-spacing:0.5px; background:linear-gradient(135deg,#7f1d1d,#991b1b); color:#fca5a5; box-shadow:0 4px 16px rgba(153,27,27,0.3)"
            @mouseover="$event.target.style.transform='translateY(-3px)'; $event.target.style.filter='brightness(1.1)'"
            @mouseout="$event.target.style.transform=''; $event.target.style.filter=''"
            @mousedown="$event.target.style.transform='scale(0.97)'"
            @mouseup="$event.target.style.transform='translateY(-3px)'">
      <span style="font-size:22px; margin-bottom:2px">✗</span>
      Nevím
      <span style="font-size:10px; font-weight:600; opacity:0.7; letter-spacing:1px; text-transform:uppercase">zapomněl jsem</span>
    </button>
    <button @click="$emit('rate', 4)"
            style="border:none; padding:18px 16px; border-radius:16px; font-size:14px; font-weight:800; cursor:pointer; transition:all 0.15s; display:flex; flex-direction:column; align-items:center; gap:4px; text-transform:uppercase; letter-spacing:0.5px; background:linear-gradient(135deg,#14532d,#166534); color:#86efac; box-shadow:0 4px 16px rgba(22,101,52,0.3)"
            @mouseover="$event.target.style.transform='translateY(-3px)'; $event.target.style.filter='brightness(1.1)'"
            @mouseout="$event.target.style.transform=''; $event.target.style.filter=''"
            @mousedown="$event.target.style.transform='scale(0.97)'"
            @mouseup="$event.target.style.transform='translateY(-3px)'">
      <span style="font-size:22px; margin-bottom:2px">✓</span>
      Umím
      <span style="font-size:10px; font-weight:600; opacity:0.7; letter-spacing:1px; text-transform:uppercase">vybavil jsem si</span>
    </button>
    <button @click="$emit('rate', 3)"
            style="border:none; padding:18px 16px; border-radius:16px; font-size:14px; font-weight:800; cursor:pointer; transition:all 0.15s; display:flex; flex-direction:column; align-items:center; gap:4px; text-transform:uppercase; letter-spacing:0.5px; background:linear-gradient(135deg,#78350f,#92400e); color:#fcd34d; box-shadow:0 4px 16px rgba(120,53,15,0.3)"
            @mouseover="$event.target.style.transform='translateY(-3px)'; $event.target.style.filter='brightness(1.1)'"
            @mouseout="$event.target.style.transform=''; $event.target.style.filter=''"
            @mousedown="$event.target.style.transform='scale(0.97)'"
            @mouseup="$event.target.style.transform='translateY(-3px)'">
      <span style="font-size:22px; margin-bottom:2px">~</span>
      Těžké
      <span style="font-size:10px; font-weight:600; opacity:0.7; letter-spacing:1px; text-transform:uppercase">s námahou</span>
    </button>
    <button @click="$emit('rate', 5)"
            style="border:none; padding:18px 16px; border-radius:16px; font-size:14px; font-weight:800; cursor:pointer; transition:all 0.15s; display:flex; flex-direction:column; align-items:center; gap:4px; text-transform:uppercase; letter-spacing:0.5px; background:linear-gradient(135deg,#1e3a8a,#1d4ed8); color:#93c5fd; box-shadow:0 4px 16px rgba(29,78,216,0.3)"
            @mouseover="$event.target.style.transform='translateY(-3px)'; $event.target.style.filter='brightness(1.1)'"
            @mouseout="$event.target.style.transform=''; $event.target.style.filter=''"
            @mousedown="$event.target.style.transform='scale(0.97)'"
            @mouseup="$event.target.style.transform='translateY(-3px)'">
      <span style="font-size:22px; margin-bottom:2px">⚡</span>
      Lehké
      <span style="font-size:10px; font-weight:600; opacity:0.7; letter-spacing:1px; text-transform:uppercase">bez problémů</span>
    </button>
  </div>
</template>

<script setup>
defineEmits(['rate'])
</script>
