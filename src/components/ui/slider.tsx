"use client"

import * as React from "react"
import { Slider as SliderPrimitive } from "@base-ui/react/slider"

import { cn } from "@/lib/utils"

const Slider = React.forwardRef<
  React.ElementRef<typeof SliderPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SliderPrimitive.Root>
>(({ className, ...props }, ref) => (
  <SliderPrimitive.Root
    ref={ref}
    className={cn(
      "relative flex w-full touch-none select-none items-center",
      className
    )}
    {...props}
  >
    <SliderPrimitive.Control className="relative flex w-full items-center">
      <SliderPrimitive.Track className="relative h-1 w-full grow overflow-hidden rounded-full bg-zinc-800">
        <SliderPrimitive.Indicator className="absolute h-full bg-indigo-500" />
      </SliderPrimitive.Track>
      <SliderPrimitive.Thumb className="block h-3.5 w-3.5 rounded-full border border-indigo-500/50 bg-white shadow transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-indigo-500 disabled:pointer-events-none disabled:opacity-50" />
    </SliderPrimitive.Control>
  </SliderPrimitive.Root>
))
Slider.displayName = "Slider"

export { Slider }
