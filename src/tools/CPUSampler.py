"""
CPUSampler - Converted from Java source
Original: tools/CPUSampler.java
Package: tools
"""

from typing import Dict
from typing import List
from typing import Optional, Any
from typing import Set
import math
import os
import threading
import time


class CPUSampler:
    """
    Class CPUSampler
    """

    def __init__(self):
        self.included = None
        self.interval = 0
        self.sampler = None
        self.recorded = None
        self.totalSamples = 0
        self.count = None
        self.trace = None
        self.running = False
        self.shouldRun = False
        self.rthread = None
        self.included = []
        self.interval = 5
        self.sampler = None
        self.recorded = {}
        self.totalSamples = 0

    # Static initializer
    # instance = CPUSampler()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def setInterval(self, millis: int) -> None:
        self.interval = millis

    def addIncluded(self, include: str) -> None:
        for alreadyIncluded in self.included:
            if include.startswith(alreadyIncluded):
                return
        self.included.add(include)

    def reset(self) -> None:
        self.recorded.clear()
        self.totalSamples = 0

    def start(self) -> None:
        if self.sampler is None:
            (self.sampler = SamplerThread()).start()

    def stop(self) -> None:
        if self.sampler is not None:
            self.sampler.stop()
            self.sampler = None

    def getTopConsumers(self) -> Any:
        ret = []
        final Set<Map.Entry<StackTrace, Integer>> entrySet = self.recorded.items()
        for (final Map.Entry<StackTrace, Integer> entry : entrySet)
            ret.add(StacktraceWithCount(entry.getValue(), entry.getKey()))
        Collections.sort(ret)
        return SampledStacktraces(ret, self.totalSamples)

    def save(self, writer: Any, minInvocations: int, topMethods: int) -> None:
        topConsumers = self.getTopConsumers()
        builder = ""
        builder.append("Top Methods:\n")
        for i in range(topMethods && i < topConsumers.getTopConsumers()):
            builder.append(topConsumers.getTopConsumers().get(i).toString(topConsumers.getTotalInvocations(), 1))
        builder.append("\nStack Traces:\n")
        writer.write(builder)
        writer.write(topConsumers.toString(minInvocations))
        writer.flush()

    def consumeStackTraces(self, traces: dict) -> None:
        for (final Map.Entry<Thread, StackTraceElement[]> trace : traces.items())
            relevant = self.findRelevantElement(trace.getValue())
            if relevant != -1:
                st = StackTrace(trace.getValue(), relevant, trace.getKey().getState())
                i = self.recorded.get(st)
                self.totalSamples += 1
                if i is None:
                    self.recorded.put(st, 1)
                else:
                    self.recorded.put(st, i + 1)

    def findRelevantElement(self, trace: list) -> int:
        if len(trace) == 0:
            return -1
        if self.included == 0:
            return 0
        firstIncluded = -1
        for myIncluded in self.included:
            for i in range(len(trace)):
                ste = trace[i]
                if ste.getClassName().startswith(myIncluded) && (i < firstIncluded || firstIncluded == -1):
                    firstIncluded = i
                    break
        if firstIncluded >= 0 && trace[firstIncluded].getClassName() == ("tools.performance.CPUSampler$SamplerThread"):
            return -1
        return firstIncluded

    def equals(self, obj: Any) -> bool:
        if !(isinstance(obj, StackTrace)):
            return False
        other = obj
        if other.len(trace) != self.len(trace):
            return False
        if other.state != self.state:
            return False
        for i in range(self.len(trace)):
            if !self.trace[i] == (other.trace[i]):
                return False
        return True

    def hashCode(self) -> int:
        ret = 13 * self.len(trace) + self.state.hashCode()
        for ste in self.trace:
            ret ^= ste.hashCode()
        return ret

    def getTrace(self) -> list:
        return self.trace

    def toString(self) -> str:
        return self.toString(-1)

    def toString_traceLength(self, traceLength: int) -> str:
        ret = ""
        ret.append(self.state.name())
        if traceLength > 1:
            ret.append("\n")
        else:
            ret.append(" ")
        i = 0
        for ste in self.trace:
            if ++i > traceLength:
                break
            ret.append(ste.getClassName())
            ret.append("#")
            ret.append(ste.getMethodName())
            ret.append(" (Line: ")
            ret.append(ste.getLineNumber())
            ret.append(")\n")
        return ret

    def getCount(self) -> int:
        return self.count

    def compareTo(self, o: Any) -> int:
        return -Integer.valueOf(self.count).compareTo(o.count)

    def equals_oth(self, oth: Any) -> bool:
        if !(isinstance(oth, StacktraceWithCount)):
            return False
        o = oth
        return self.count == o.count

    def getPercentage(self, total: int) -> float:
        return Math.round(self.count / total * 10000.0) / 100.0

    def toString_totalInvoations_traceLength(self, totalInvoations: int, traceLength: int) -> str:
        return self.count + "/" + totalInvoations + " Sampled Invocations (" + self.getPercentage(totalInvoations) + "%) " + self.trace.toString(traceLength)

    def getTotalInvocations(self) -> int:
        return self.totalInvocations

    def toString_minInvocation(self, minInvocation: int) -> str:
        ret = ""
        for swc in self.topConsumers:
            if swc.getCount() >= minInvocation:
                ret.append(swc.toString(self.totalInvocations, Integer.MAX_VALUE))
                ret.append("\n")
        return ret

    def run(self) -> None:
        while self.shouldRun:
            CPUSampler.self.consumeStackTraces(Thread.getAllStackTraces())
            try:
                Thread.sleep(CPUSampler.self.interval)
                continue
            except InterruptedException as e:
                return


# Inner class from Java (originally nested)
class StackTrace:
    """
    Class StackTrace
    """

    def __init__(self, trace: list, startAt: int, state: Any):
        self.state = state
        if startAt == 0:
            self.trace = trace
        else:
            System.arraycopy(trace, startAt, self.trace = new StackTraceElement[len(trace) - startAt], 0, self.len(trace))


    def equals(self, obj: Any) -> bool:
        if !(isinstance(obj, StackTrace)):
            return False
        other = obj
        if other.len(trace) != self.len(trace):
            return False
        if other.state != self.state:
            return False
        for i in range(self.len(trace)):
            if !self.trace[i] == (other.trace[i]):
                return False
        return True

    def hashCode(self) -> int:
        ret = 13 * self.len(trace) + self.state.hashCode()
        for ste in self.trace:
            ret ^= ste.hashCode()
        return ret

    def getTrace(self) -> list:
        return self.trace

    def toString(self) -> str:
        return self.toString(-1)

    def toString_traceLength(self, traceLength: int) -> str:
        ret = ""
        ret.append(self.state.name())
        if traceLength > 1:
            ret.append("\n")
        else:
            ret.append(" ")
        i = 0
        for ste in self.trace:
            if ++i > traceLength:
                break
            ret.append(ste.getClassName())
            ret.append("#")
            ret.append(ste.getMethodName())
            ret.append(" (Line: ")
            ret.append(ste.getLineNumber())
            ret.append(")\n")
        return ret


# Inner class from Java (originally nested)
class StacktraceWithCount:
    """
    Class StacktraceWithCount
    Implements: Comparable<StacktraceWithCount>
    """

    def __init__(self, count: int, trace: Any):
        self.count = None
        self.trace = None
        self.count = count
        self.trace = trace


    def getCount(self) -> int:
        return self.count

    def getTrace(self) -> list:
        return self.trace.getTrace()

    def compareTo(self, o: Any) -> int:
        return -Integer.valueOf(self.count).compareTo(o.count)

    def equals(self, oth: Any) -> bool:
        if !(isinstance(oth, StacktraceWithCount)):
            return False
        o = oth
        return self.count == o.count

    def toString(self) -> str:
        return self.count + " Sampled Invocations\n" + self.trace

    def getPercentage(self, total: int) -> float:
        return Math.round(self.count / total * 10000.0) / 100.0

    def toString_totalInvoations_traceLength(self, totalInvoations: int, traceLength: int) -> str:
        return self.count + "/" + totalInvoations + " Sampled Invocations (" + self.getPercentage(totalInvoations) + "%) " + self.trace.toString(traceLength)


# Inner class from Java (originally nested)
class SampledStacktraces:
    """
    Class SampledStacktraces
    """

    def __init__(self, topConsumers: list, totalInvocations: int):
        self.topConsumers = topConsumers
        self.totalInvocations = totalInvocations


    def getTopConsumers(self) -> list:
        return self.topConsumers

    def getTotalInvocations(self) -> int:
        return self.totalInvocations

    def toString(self) -> str:
        return self.toString(0)

    def toString_minInvocation(self, minInvocation: int) -> str:
        ret = ""
        for swc in self.topConsumers:
            if swc.getCount() >= minInvocation:
                ret.append(swc.toString(self.totalInvocations, Integer.MAX_VALUE))
                ret.append("\n")
        return ret


# Inner class from Java (originally nested)
class SamplerThread(Runnable):
    """
    Class SamplerThread
    Implements: Runnable
    """

    def __init__(self):
        self.running = False
        self.shouldRun = False
        self.rthread = None
        self.running = False
        self.shouldRun = False


    def start(self) -> None:
        if !self.running:
            self.shouldRun = True
            (self.rthread = Thread(this, "CPU Sampling Thread")).start()
            self.running = True

    def stop(self) -> None:
        self.shouldRun = False
        self.rthread.interrupt()
        try:
            self.rthread.join()
        except InterruptedException as e:
            e.printStackTrace()

    def run(self) -> None:
        while self.shouldRun:
            CPUSampler.self.consumeStackTraces(Thread.getAllStackTraces())
            try:
                Thread.sleep(CPUSampler.self.interval)
                continue
            except InterruptedException as e:
                return

