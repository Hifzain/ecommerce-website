function calculateTotalLoad() {
  let totalEnergyUsage = 0; 
  const appliances = [
      { id: 'led_bulb_qty', wattage: 7, hours: 'led_bulb_hours' },
      { id: 'led_tv_qty', wattage: 50, hours: 'led_tv_hours' },
      { id: 'refrigerator_qty', wattage: 350, hours: 'refrigerator_hours' },
      { id: 'freezer_qty', wattage: 350, hours: 'freezer_hours' },
      { id: 'washing_machine_qty', wattage: 800, hours: 'washing_machine_hours' },
      { id: 'fan_qty', wattage: 100, hours: 'fan_hours' },
      { id: 'iron_qty', wattage: 1000, hours: 'iron_hours' },
      { id: 'ac_1ton_qty', wattage: 1800, hours: 'ac_1ton_hours' },
      { id: 'split_ac_1_5ton_qty', wattage: 2400, hours: 'split_ac_1_5ton_hours' },
  ];

  appliances.forEach(function(appliance) {
      let quantity = parseInt(document.getElementById(appliance.id).value) || 0;
      let hours = parseInt(document.getElementById(appliance.hours).value) || 0;
      totalEnergyUsage += (quantity * appliance.wattage * hours);
  });
    
    for (let i = 1; i < applianceCounter; i++) {
      const wattageField = document.getElementById(`wattage-${i}`);
      const quantityField = document.getElementById(`quantity-${i}`);
      const hoursField = document.getElementById(`hours-${i}`);

      if (wattageField && quantityField && hoursField) {
          const wattage = parseInt(wattageField.value) || 0;
          const quantity = parseInt(quantityField.value) || 0;
          const hours = parseInt(hoursField.value) || 0;

          totalEnergyUsage += (wattage * quantity * hours);
      }
  }
  let totalEnergyKWh = totalEnergyUsage / 1000;

  
  let sunHours = parseFloat(document.getElementById('average_sun_hours').value) || 6;
  let systemSizeKW = (totalEnergyKWh / sunHours) * 0.8; // Add a 20% safety margin for losses


  document.getElementById('total-load').textContent = 'Total Energy Usage: ' + totalEnergyKWh.toFixed(2) + ' kWh/day';
  document.getElementById('system-size').textContent = 'Required System Size: ' + systemSizeKW.toFixed(2) + ' kW';
}



function resetForm() {
  document.getElementById("calculator-form").reset(); // Reset all form values
  document.getElementById('total-load').textContent = 'Total Energy Usage: 0 kWh/day';
  document.getElementById('system-size').textContent = 'Required System Size: 0 kW';
}