import bar
import network.stream

if __name__ == '__main__':
    #bar.run() # run on local device with bars to examine the output.
    stream = network.stream.app.run(host="0.0.0.0", port=5009) # direct the output to a local route.