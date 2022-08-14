#!/usr/bin/env python3
import sys
import argparse
import time
import rclpy
from rclpy.node import Node
from dragonfly_messages.srv import Pump
import rx
import rx.operators as ops
from rx.scheduler import NewThreadScheduler


class BagInflateService(Node):
    def __init__(self, arg_id, sim=False):
        super().__init__('bag_inflate_service')
        self.id = arg_id
        self.sim = sim
        self.bag_gpio_pins = [16, 19, 20, 21]
        if not self.sim:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.bag_gpio_pins, GPIO.OUT)
        self.bag_full = [False] * len(self.bag_gpio_pins)
        self.inflate = self.create_service(Pump, "/{}/pump".format(self.id), self.bag_inflate_callback)
        # self.swap = self.create_service(BagSwap, "/{}/bagswap".format(self.id), self.bag_swap_callback)

    def bag_swap_callback(self, request, response):
        self.get_logger().info("Bags swapped")
        self.bag_full = [False] * len(self.bag_gpio_pins)
        return True

    def bag_inflate_callback(self, request, response):
        # @TODO add timestamp and id ect
        response.done = False
        self.get_logger().info("Bag {} inflate request received".format(request.pump_num))
        if not self.bag_full[request.pump_num]:
            self.bag_full[request.pump_num] = True
            response.done = True
            if not self.sim:
                rx.just(self.bag_gpio_pins[request.pump_num]).pipe(
                    ops.observe_on(NewThreadScheduler())) \
                    .subscribe(on_next=lambda pin: self.pump(pin))
        else:
            self.get_logger().warn("Bag {} already inflated".format(request.pump_num))
        return response

    def pump(self, pin):
        if not self.sim:
            GPIO.output(pin, 1)
            time.sleep(60)
            GPIO.output(pin, 0)


def main(args=None):
    parser = argparse.ArgumentParser(description='Sample Bag Collection Service')
    parser.add_argument('id', type=str, help='Name of the drone.')
    parser.add_argument('sim', type=bool, help='Is the sim running')
    args = parser.parse_args()
    rclpy.init(args=sys.argv)
    bag_inflate_service = BagInflateService(args.id, args.sim)
    rclpy.spin(bag_inflate_service)
    rclpy.shutdown()
    GPIO.cleanup()


if __name__ == '__main__':
    main(args=sys.argv)
