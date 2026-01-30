import { SmoothScroll } from "@/components/smooth-scroll"
import { Navbar } from "@/components/navbar"
import { SplineHero } from "@/components/spline-hero"
import { LogoMarquee } from "@/components/logo-marquee"
import { BentoGrid } from "@/components/bento-grid"
import { Pricing } from "@/components/pricing"
import { FinalCTA } from "@/components/final-cta"
import { Footer } from "@/components/footer"
import { LoadingScreen } from "@/components/loading-screen"

export default function Home() {
  return (
    <>
      <LoadingScreen />
      <SmoothScroll>
        <main className="bg-zinc-950">
          <Navbar />
          <SplineHero />
          <LogoMarquee />
          <BentoGrid />
          <Pricing />
          <FinalCTA />
          <Footer />
        </main>
      </SmoothScroll>
    </>
  )
}
