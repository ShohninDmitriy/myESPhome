import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import sensor, switch, output, time
from esphome.const import (
    CONF_ID,
    STATE_CLASS_MEASUREMENT,
)
CONF_ACTIVATION_ID = 'activation_id'
CONF_INPUT_ID = 'input_id'
CONF_SETPOINT = 'setpoint'
CONF_KP = 'kp'
CONF_KI = 'ki'
CONF_KD = 'kd'
CONF_OUTPUT_ID = 'output_id'
CONF_OUTPUT_MIN = 'output_min'
CONF_OUTPUT_MAX = 'output_max'
CONF_POWER_ID = 'power_id'
CONF_PWM_RESTART = 'pwm_restart'
CONF_ERROR = 'error'
CONF_PWM_OUTPUT = 'pwm_output'

CONF_NEW_SETPOINT = 'new_setpoint'
CONF_NEW_KP = 'new_kp'
CONF_NEW_KI = 'new_ki'
CONF_NEW_KD = 'new_kd'
CONF_NEW_OUTPUT_MIN = 'new_output_min'
CONF_NEW_OUTPUT_MAX = 'new_output_max'
CONF_NEW_PWM_RESTART = 'new_pwm_restart'

# from esphome.core.entity_helpers import inherit_property_from

CODEOWNERS = ["@SeByDocKy"]
DEPENDENCIES = ["time"]

### Sensor component ####
solarpid_ns = cg.esphome_ns.namespace("solarpid")
SOLARPID = solarpid_ns.class_(
    "SOLARPID", sensor.Sensor, switch.Switch, binary_sensor.BinarySensor, cg.Component
)

### Actions ###
# SetPointAction = solarpid_ns.class_('SetPointAction', automation.Action)

# SetKpAction = solarpid_ns.class_('SetKpAction', automation.Action)
# SetKiAction = solarpid_ns.class_('SetKiAction', automation.Action)
# SetKdAction = solarpid_ns.class_('SetKdAction', automation.Action)

# SetOutputMinAction = solarpid_ns.class_('SetOutputMinAction', automation.Action)
# SetOutputMaxAction = solarpid_ns.class_('SetOutputMaxAction', automation.Action)

# SetPwmRestartAction = solarpid_ns.class_('SetPwmRestartAction', automation.Action)

# PidUpdateAction = solarpid_ns.class_('PidUpdateAction', automation.Action)

CONFIG_SCHEMA = (
    cv.Schema(
        {
	    cv.GenerateID(): cv.declare_id(SOLARPID),
	    # cv.Required(CONF_ACTIVATION_ID): cv.use_id(binary_sensor.BinarySensor),
            cv.Required(CONF_ACTIVATION_ID): cv.use_id(switch.Switch), 	  	
	    cv.Required(CONF_INPUT_ID): cv.use_id(sensor.Sensor),
	    cv.Required(CONF_OUTPUT_ID): cv.use_id(output.FloatOutput),
	    cv.Optional(CONF_SETPOINT, default=0.0): cv.float_,
	    cv.Optional(CONF_KP, default=0.1): cv.float_,
	    cv.Optional(CONF_KI, default=0.0): cv.float_,
	    cv.Optional(CONF_KD, default=0.0): cv.float_,
	    cv.Optional(CONF_OUTPUT_MIN, default=0.0):  cv.float_range(min=0.0, max=1.0),
	    cv.Optional(CONF_OUTPUT_MAX, default=1.0): cv.float_range(min=0.0, max=1.0),
	    cv.Optional(CONF_POWER_ID): cv.use_id(sensor.Sensor),
	    cv.Optional(CONF_PWM_RESTART, default=0.0): cv.float_range(min=0.0, max=1.0),
	    cv.Optional(CONF_ERROR): sensor.sensor_schema(
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
             ),
	    cv.Optional(CONF_PWM_OUTPUT): sensor.sensor_schema(
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
             ),
	}
     )
    .extend(cv.polling_component_schema("60s"))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    switch_sens = await cg.get_variable(config[CONF_ACTIVATION_ID])
    cg.add(var.set_activation_switch(switch_sens))
	
    sens = await cg.get_variable(config[CONF_INPUT_ID])
    cg.add(var.set_input_sensor(sens))
	
    out = await cg.get_variable(config[CONF_OUTPUT_ID])
    cg.add(var.set_output(out))
	
    if CONF_SETPOINT in config:
        cg.add(var.set_setpoint(config[CONF_SETPOINT]))
	
    if CONF_KP in config:
        cg.add(var.set_kp(config[CONF_KP]))
	    
    if CONF_KI in config:
        cg.add(var.set_ki(config[CONF_KI]))

    if CONF_KD in config:
        cg.add(var.set_kd(config[CONF_KD]))

    if CONF_OUTPUT_MIN in config:
        cg.add(var.set_output_min(config[CONF_OUTPUT_MIN]))

    if CONF_OUTPUT_MAX in config:
        cg.add(var.set_output_max(config[CONF_OUTPUT_MAX]))

    if CONF_POWER_ID in config:
        sens = await cg.get_variable(config[CONF_POWER_ID])
        cg.add(var.set_power_sensor(sens))
	   
    if CONF_PWM_RESTART in config:
        cg.add(var.set_pwm_restart(config[CONF_PWM_RESTART]))
		
    if CONF_ERROR in config:
        sens = await sensor.new_sensor(config[CONF_ERROR])
        cg.add(var.set_error(sens))

    if CONF_PWM_OUTPUT in config:
        sens = await sensor.new_sensor(config[CONF_PWM_OUTPUT])
        cg.add(var.set_pwm_output(sens))		

# @automation.register_action(
#     "solarpid.set_point",
#     SetPointAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_SETPOINT): cv.templatable(cv.float_range(min=0.0, max=1.0)),
#         }
#     ),
# )
# async def set_point_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_set_point = await cg.templatable(config[CONF_NEW_SETPOINT], args, float_) 
#     cg.add(var.set_new_setpoint(template_new_set_point))	
#     return var


# @automation.register_action(
#     "solarpid.set_kp",
#     SetKpAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_KP): cv.templatable(cv.float_),
#         }
#     ),
# )

# async def set_kp_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_kp = await cg.templatable(config[CONF_NEW_KP], args, float_) 
#     cg.add(var.set_new_kp(template_new_kp))	
#     return var


# @automation.register_action(
#     "solarpid.set_ki",
#     SetKiAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_KI): cv.templatable(cv.float_),
#         }
#     ),
# ) 

# async def set_ki_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_ki = await cg.templatable(config[CONF_NEW_KI], args, float_) 
#     cg.add(var.set_new_ki(template_new_ki))	
#     return var


# @automation.register_action(
#     "solarpid.set_kd",
#     SetKdAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_KD): cv.templatable(cv.float_),
#         }
#     ),
# )
# async def set_kd_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_kd = await cg.templatable(config[CONF_NEW_KD], args, float_) 
#     cg.add(var.set_new_kd(template_new_kd))	
#     return var


# @automation.register_action(
#     "solarpid.set_output_min",
#     SetOutputMinAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_OUTPUT_MIN): cv.templatable(cv.float_range(min=0.0, max=1.0)),
#         }
#     ),
# )
# async def set_output_min_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_output_min = await cg.templatable(config[CONF_NEW_OUTPUT_MIN], args, float_) 
#     cg.add(var.set_new_output_min(template_new_output_min))	
#     return var


# @automation.register_action(
#     "solarpid.set_output_max",
#     SetOutputMaxAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_OUTPUT_MAX): cv.templatable(cv.float_range(min=0.0, max=1.0)),
#         }
#     ),
# )
# async def set_output_max_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_output_max = await cg.templatable(config[CONF_NEW_OUTPUT_MAX], args, float_) 
#     cg.add(var.set_new_output_max(template_new_output_max))	
#     return var

# @automation.register_action(
#     "solarpid.set_pwm_restart",
#     SetPwmRestartAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
# 	    cv.Required(CONF_NEW_PWM_RESTART): cv.templatable(cv.float_range(min=0.0, max=1.0)),
#         }
#     ),
# )
# async def set_pwm_restart_to_code(config, action_id, template_arg, args):
#     parent = await cg.get_variable(config[CONF_ID])
#     var = cg.new_Pvariable(action_id, template_arg , parent)
#     template_new_pwm_restart = await cg.templatable(config[CONF_PWM_RESTART], args, float_) 
#     cg.add(var.set_new_pwm_restart(template_new_pwm_restart))	
#     return var

# @automation.register_action(
#     "solarpid.pid_update",
#     PidUpdateAction,
#     maybe_simple_id(
#         {
#             cv.Required(CONF_ID): cv.use_id(SOLARPID),
#         }
#     ),
# )
