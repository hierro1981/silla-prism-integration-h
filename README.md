#  # Silla Prism Solar custom integration

![Silla Prism Solar](image.png)

This repository contains a fork of the custom integration to integrate a Silla Prism EVSE inside HomeAssistant made by https://github.com/persuader72/silla-prism-integration

## Installation

Prerequisites: A working MQTT server.

1) Configure the Prism EVSE to work with your MQTT server  [has shown in manual](https://support.silla.industries/wp-content/uploads/2023/09/DOC-Prism_MQTT_Manual-rel.2.0_rev.-20220105-EN.pdf).
2) Configure and enable the [MQTT integration](https://www.home-assistant.io/integrations/mqtt/) for HomeAssistant
3) Install the custom integration from this repository [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=https%3A%2F%2Fgithub.com%2Fhierro1981%2Fsilla-prism-integration-h&owner=Hierro)

## Usage

1. Add integration Silla Prism using the dashboard  [![Open your Home Assistant instance and start setting up a new integration of a specific brand.](https://my.home-assistant.io/badges/brand.svg)](https://my.home-assistant.io/redirect/brand/?brand=silla_prism) 

2. Keep note of base path for all Prism topics

   ![Prism manual](images/setup3.png)

3. **Topic** Set the the base path for all Prism topics must be the same set in the Prism configuration page seen before. For now it is important to leave a **/** at the end of the topic as shown in the picture below)

4. **number of ports ** If you have more the one port (like Prism Duo) on your device set here the corresponding number of ports otherwise if you have only one port you can leave this field at the default value of 1

5. **serial number** or **unique code** if you have more then one Prism connected to HomeAssistant you have to fill this value with a unique code (you can use the serial number) otherwise if you have only one Prism you can leave this field blank.

6. **Enable virtual sensor** this enable additional sensors derived from the original Prism sensors, like the counter of the total energy consumed from the power grid. 

7. ![Configure Silla Prism](images/setup2.png)

## Solar automations

Solar automation is a work in progress. And we be described in [Solar](solar.md) page 

## Entities

| Entity ID                         | Type         | Description                                                  | Unit                                   |
| --------------------------------- | ------------ | ------------------------------------------------------------ | -------------------------------------- |
| silla_prism_online                | BinarySensor | Sensor to find if Prism is connected or not                  |                                        |
| silla_prism_current_state         | Sensor       | Current state of Prism                                       | "idle", "waiting", "charging", "pause" |
| silla_prism_power_grid_voltage    | Sensor       | Measured voltage from grid                                   | V                                      |
| silla_prism_output_power          | Sensor       | Power provided to the charging port                          | W                                      |
| silla_prism_output_current        | Sensor       | Current provided to the charging port                        | mA                                     |
| silla_prism_output_car_current    | Sensor       | Current driven by the car                                    | A                                      |
| silla_prism_current_set_by_user   | Sensor       | Current limit set by user                                    | A                                      |
| silla_prism_session_time          | Sensor       | Duration of the current session                              | s                                      |
| silla_prism_session_output_energy | Sensor       | Energy provided to the charging port during the current session | Wh                                     |
| silla_prism_total_output_energy   | Sensor       | Total energy                                                 | Wh                                     |
| ?/1/error                         | (TODO)       | Error code                                                   |                                        |
| silla_prism_current_port_mode     | Sensor       | Current port mode                                            | solar,normal,paused                    |
| silla_prism_input_grid_power      | Sensor       | Input power from grid                                        | W                                      |
| silla_prism_set_max_current       | Number       | Set the user current limit                                   | A                                      |
| silla_prism_set_current_limit     | Number       | Set the  current limit                                       | A                                      |
| silla_prism_set_mode              | Select       | Set current port mode                                        | solar,normal,paused                    |
| silla_prism_touch_sigle           | BinarySensor | Goes on for 1 second after a single touch gesture            | On,Off                                 |
| silla_prism_touch_double          | BinarySensor | Goes on for 1 second after a double touch gesture            | On,Off                                 |
| silla_prism_touch_long            | BinarySensor | Goes on for 1 second after a long touch gesture              | On,Off                                 |

## Computed Entities

Computed entities are not directly measured from Prism but are derived from other measurements. 

| Entity ID                     | Type   | Description                  | Unit |
| ----------------------------- | ------ | ---------------------------- | ---- |
| silla_prism_input_grid_energy | Sensor | Total energy taken from grid | Wh   |
|                               |        |                              |      |
|                               |        |                              |      |



## Charger Card Integragtion

![Charger](images/setup4.png)

It's possible to configure the [EV Charger Card](https://github.com/tmjo/charger-card) using the configuration example [provided](https://github.com/hierro1981/silla-prism-integration-h/blob/main/charger-card/template.yaml) in this repository 

# Touch button and Automations

This are some example automations for the touch button events

### Start charge after single touch event if Prism is in pause state

```yaml
alias: Avvia ricarica dopo pressione pulsante
description: Avvia ricarica dopo pressione pulsante
trigger:
  - platform: state
    entity_id:
      - binary_sensor.silla_prism_touch_sigle
    from: "off"
    to: "on"
condition:
  - condition: state
    entity_id: sensor.silla_prism_current_state
    state: pause
action:
  - service: select.set_option
    data:
      entity_id: select.silla_prism_set_mode
      option: normal
mode: single
```

### Stop charge after single touch event if Prism is in charging state

```yaml
alias: Interrompi ricarica dopo pressione pulsante
description: Interrompi ricarica dopo pressione pulsante
trigger:
  - platform: state
    entity_id:
      - binary_sensor.silla_prism_touch_sigle
    from: "off"
    to: "on"
condition:
  - condition: state
    entity_id: sensor.silla_prism_current_state
    state: charging
action:
  - service: select.set_option
    data:
      entity_id: select.silla_prism_set_mode
      option: paused
mode: single
```

