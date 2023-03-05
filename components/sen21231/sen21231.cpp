#include "sen21231.h"
#include "esphome/core/log.h"

namespace esphome {
namespace sen21231 {

static const char *const TAG = "sen21231";

void SEN21231Component::update() { this->read_data_(); }

float SEN21231Component::get_setup_priority() const { return setup_priority::DATA; }

void SEN21231Component::dump_config() {
  ESP_LOGCONFIG(TAG, "SEN21231:");
  LOG_I2C_DEVICE(this);
  if (this->is_failed()) {
    ESP_LOGE(TAG, "Communication with SEN21231 failed!");
  }
  ESP_LOGI(TAG, "%s", this->is_failed() ? "FAILED" : "OK");
  LOG_UPDATE_INTERVAL(this);
}

void SEN21231Component::read_data_() {
  person_sensor_results_t results;
  this->read_bytes(PERSON_SENSOR_I2C_ADDRESS, (uint8_t *) &results, sizeof(results));
  
  if (this->nfaces_sensor_ != nullptr) {
	  this->nfaces_sensor_->publish_state(results.num_faces);
  }
  ESP_LOGD(TAG, "%d faces detected", results.num_faces);
  
  if (results.num_faces == 1) {
	
	if (this->conf0_sensor_ != nullptr) {
	  this->conf0_sensor_->publish_state(int(results.faces[0].box_confidence) );
	}
	ESP_LOGD(TAG, "conf0: %d", results.faces[0].box_confidence);
	
	if (this->x0_sensor_ != nullptr) {
	  this->x0_sensor_->publish_state(int(results.faces[0].box_left));
	}
	ESP_LOGD(TAG, "x0: %d", results.faces[0].box_left);
	
	if (this->y0_sensor_ != nullptr) {
	  this->y0_sensor_->publish_state(int(results.faces[0].box_top));
	} 
    ESP_LOGD(TAG, "y0: %d", results.faces[0].box_top);
	
	if (this->w0_sensor_ != nullptr) {
	  this->w0_sensor_->publish_state(int(results.faces[0].box_right));
	} 
    ESP_LOGD(TAG, "w0: %d", results.faces[0].box_right);
    
	if (this->h0_sensor_ != nullptr) {
	  this->h0_sensor_->publish_state(int(results.faces[0].box_bottom));
	}
	ESP_LOGD(TAG, "height: %d", results.faces[0].box_bottom);	
    
	if (this->isfacing0_sensor_ != nullptr) {
	  this->isfacing0_sensor_->publish_state(int(results.faces[0].is_facing));
	}
	ESP_LOGD(TAG, "is facing towards camera: %d", results.faces[0].is_facing);
  }
/*  
  else{
	  this->conf0_sensor_->publish_state(-1);
	  this->x0_sensor_->publish_state(-1);
	  this->y0_sensor_->publish_state(-1);
	  this->w0_sensor_->publish_state(-1);
	  this->h0_sensor_->publish_state(-1);
	  this->isfacing0_sensor_->publish_state(-1);
  }
*/  
}

}  // namespace sen21231
}  // namespace esphome
