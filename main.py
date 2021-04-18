
import simpy
import random
import matplotlib.pyplot as plt

# Use simpy to simulate toyota automobile's production
class Toyota_Factory:
    def __init__(self, env):
        # input process
        self.machinery = simpy.Container(env, capacity=machinery_capacity, init=initial_machinery)
        self.machinery_control = env.process(self.machinery_stock_control(env))
        self.components = simpy.Container(env, capacity=components_capacity, init=initial_components)
        self.components_control = env.process(self.components_stock_control(env))
        self.assembler = simpy.Container(env, capacity=assembler_capacity, init=0)
        self.assembler_control = env.process(self.assembler_stock_control(env))

        # activities
        #self.parts_sequencing = env.process(self.parts_sequencing_control(env))
        #self.setting_up_schedule = env.process(self.setting_up_schedule_control(env))
        #self.production_commence = env.process(self.production_commence_control(env))

        # output
        #self.quality_check = env.process(self.quality_check_control(env))
        #self.vehicle_assemble = env.process(self.vehicle_assemble_control(env))

        self.dispatch = simpy.Container(env, capacity=dispatch_capacity, init=0)
        self.dispatch_control = env.process(self.dispatch_vehicle_control(env))

        # Closure & monitor
        #self.transport_dealer = env.process(self.transport_dealer_control(env))
        self.env_status_monitor = env.process(self.env_status(env))

    def machinery_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.machinery.level <= machinery_critial_stock:
                print('vehicle machinery storage ({0})below the warning storage level DAY={1},HOUR={2}'.format(
                    self.machinery.level,int(env.now / 8), env.now % 8))
                print('please contact toyota of japan！')
                print('----------------------------------')
                yield env.timeout(16)
                print('vehicle machinery arrived.  DAY = {0}, HOUR={1}'.format(int(env.now / 8), env.now % 8))

                yield self.machinery.put(300)
                print('vehicle machinery storage added to {0}'.format(
                    self.machinery.level))
                print('----------------------------------')
                yield env.timeout(8*2)
            else:
                yield env.timeout(1)

    def components_stock_control(self, env):
        yield env.timeout(0)
        while True:
            if self.components.level <= components_critical_stock:
                print('components storage ({0}) below warning storage.DAY={1},HOUR={2}'.format(
                    self.components.level, int(env.now / 8), env.now % 8))
                print('please contact the components department of toyota')
                print('----------------------------------')
                yield env.timeout(9)
                print('components arrived.DAY={0},HOUR={1}'.format(
                    int(env.now / 8), env.now % 8))
                yield self.components.put(300)
                print('storage components are added up to {0}'.format(
                    self.components.level))
                print('----------------------------------')
                yield env.timeout(8*2)
            else:
                yield env.timeout(1)

    def assembler_stock_control(self, env):
        global vehicle_made
        yield env.timeout(0)
        while True:
            if self.assembler.level >= dispatch_max_capacity:
                print('assembler storage is ：{0}, waiting for production commence. DAY:{1},HOUR:{2}'.format(self.assembler.level, int(env.now / 8), env.now % 8))
                print('xxxxxxxxxxxxxxxxxxx')
                yield env.timeout(4)
                print('production commence take {0}  machinery and {1} components.  DAY:{2},HOUR:{3}' .format(self.machinery.level,self.components.level,int(env.now / 8), env.now % 8))
                yield self.assembler.get(self.assembler.level)
                print('xxxxxxxxxx')
                yield env.timeout(8*2)
            else:
                yield env.timeout(1)


    def dispatch_vehicle_control(self,env):
        yield env.timeout(0)
        while True:
            if self.dispatch.level >= 50:
                print('dispatch storage is ：{0}, waiting for transform to dealer. DAY={1},HOUR={2}'.format(
                    self.dispatch.level, int(env.now / 8), env.now % 8))
                print('----------------------------------')
                yield env.process(self.transport_dealer(env))
                print('----------------------------------')
                yield env.timeout(8*2)
            else:
                yield env.timeout(1)

    def transport_dealer(self,env):
        dealer_time = max(1,int(abs(random.gauss(mean_dealer, std_dealer))))
        yield env.timeout(dealer_time)
        dealer_get = int(self.dispatch.level/2)
        yield self.dispatch.get(dealer_get)
        print('dealer take {0}  vehicles. DAY={1},HOUR={2}'.format(dealer_get,int(env.now / 8), env.now % 8))

    def env_status(self, env):
        current_x_list = []
        current_y_list = []
        while True:
            plt.title('dispatch by superman')
            print('storage of dispatch：{0}. DAY={1}, HOUR={2}'.format(self.dispatch.level,int(env.now / 8),env.now % 8))
            current_x_list.append(env.now/8)
            current_y_list.append(self.dispatch.level)
            plt.clf()
            plt.plot(current_x_list,current_y_list,ls='-',lw=2,color='#ff7f0e')
            plt.show()
            plt.pause(0.001)
            yield env.timeout(1)

def assembler(env, toyoto_factory):
    while True:
        yield toyoto_factory.machinery.get(10)
        yield toyoto_factory.components.get(10)
        assembler_time = abs(random.gauss(mean_assembler, std_assembler))
        yield env.timeout(assembler_time)
        # wait for quality check finished
        quality_check_time = abs(random.gauss(mean_quality_check,std_quality_check))
        yield env.timeout(quality_check_time)
        yield toyoto_factory.dispatch.put(10)

def dispatcher(env,toyoto_factory):
    while True:
        # wait to be transported to the dealer
        dealer_time = abs(random.gauss(mean_dealer, std_dealer))
        yield env.timeout(dealer_time)
        yield toyoto_factory.dispatch.get(1)

# Generators
def assembler_gen(env, toyoto_factory):
    for i in range(num_assembler):
        env.process(assembler(env, toyoto_factory))
        yield env.timeout(0)
# Generators
def dispatcher_gen(env, toyoto_factory):
    for i in range(num_dispatcher):
        env.process(dispatcher(env, toyoto_factory))
        yield env.timeout(0)

if __name__ == '__main__':


    vehicle_made = 0

    print('simulation begins：')
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    # 8 hours /day
    hours = 8
    # 30 days /month
    days = 30
    # total time unit
    total_time = hours * days
    # init storage capacity
    machinery_capacity = 300
    components_capacity = 300
    assembler_capacity = 300
    dispatch_capacity = 300


    # initial machinery and components storage capacity
    initial_machinery = 100
    initial_components = 100

    dispatch_max_capacity = 80

    num_machinery = 2
    mean_machinery = 1
    std_machinery = 0.1

    num_components = 2
    mean_components = 1
    std_components = 0.1

    num_assembler = 2
    mean_assembler = 1
    std_assembler = 0.1

    num_dispatcher = 2
    mean_dispatcher = 1
    std_dispatcher = 0.1

    mean_dealer = 1
    std_dealer = 0.2
    mean_dealer_get = 1
    std_dealer_get = 0.2

    mean_quality_check = 1
    std_quality_check =0.2
    # machinery storage warning capacity
    machinery_critial_stock = (4 / mean_machinery) * num_machinery
    # components storage warning capacity
    components_critical_stock = (4 / mean_components) * num_components

    env = simpy.Environment()

    toyota_factory = Toyota_Factory(env)
    vehicle_gen = env.process(assembler_gen(env, toyota_factory))
    dispatch_gen = env.process(dispatcher_gen(env, toyota_factory))

    env.run(until=total_time)

    print('current machinery store \'s number：{0};current components store \' number： {1}'.format(
        toyota_factory.machinery.level, toyota_factory.components.level))
    print('current in assembler\' store number：{0};current in dispatcher\' store number： {1}'.format(
        toyota_factory.assembler.level, toyota_factory.dispatch.level))
    print('in this circle the total vehicle number is : {0}'.format(vehicle_made + toyota_factory.dispatch.level))
    print(f'----------------------------------')
    print(f'----------------------------------')
    print(f'simulation finished！')
